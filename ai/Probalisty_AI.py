from abc import ABC, abstractmethod
import numpy as np
from collections import deque
from ai.ai_strategy import AIStrategy
import random


class OptimizedProbabilityAI(AIStrategy):
    def __init__(self, board_size=10, ship_sizes=[5, 4, 3, 3, 2]):
      
        super().__init__(board_size)
        self.name = "Optimized Probability AI"
        self.description = "Uses probability density maps with adaptive targeting"

        # Game state tracking
        self.ship_sizes = sorted(ship_sizes, reverse=True)
        self.shots_fired = np.zeros((board_size, board_size), dtype=bool)
        self.hits = np.zeros((board_size, board_size), dtype=bool)
        self.misses = np.zeros((board_size, board_size), dtype=bool)
        self.probability_map = np.zeros((board_size, board_size))
        self.remaining_ships = self.ship_sizes.copy()

        # Track shots to avoid redundancy
        self.next_shots = []

        self.last_move = None  # Track the last move to avoid repetition

        # Enhanced ship tracking
        self.hunt_mode = True
        self.current_ship_hits = []  
        self.ship_direction = None   
        self.potential_targets = []  

        # For ship identification
        self.ship_hit_map = {}  
        self.next_ship_id = 1   
        self.sunk_ships = set()  
        self.ship_size_map = {} 

        # Parity map for optimal hunting
        self.parity_mask = np.zeros((board_size, board_size), dtype=bool)
        self._initialize_parity_mask()

        # New: Add heatmap for initial probability bias
        self.heat_map = np.ones((board_size, board_size))
        self._initialize_heat_map()

        # New: Performance optimization
        self.valid_placement_cache = {}

        # Calculate initial probability map
        self.update_probability_map()

        # Game history for learning
        self.game_history = []

    def _initialize_heat_map(self):
       
        center = self.board_size // 2

        for y in range(self.board_size):
            for x in range(self.board_size):
                # Calculate distance from center (0.0 to 1.0 range)
                dist_from_center = (
                    (y - center)**2 + (x - center)**2)**0.5 / (2*center)
                # Inverse of distance (higher in center)
                self.heat_map[y, x] = 1.0 + (1.0 - dist_from_center) * 0.2
        np.set_printoptions(precision=3)
        print(self.heat_map)

    def _initialize_parity_mask(self):
      
        largest_ship = self.ship_sizes[0]

        # Create more efficient parity pattern
        for r in range(self.board_size):
            for c in range(self.board_size):
                # Modified pattern that maximizes coverage
                if (r + c) % max(2, largest_ship // 2) == 0:
                    self.parity_mask[r, c] = True

    def _can_place_ship(self, row, col, size, orientation):
       
        # Use cache for performance
        cache_key = (row, col, size, orientation)
        if cache_key in self.valid_placement_cache:
            return self.valid_placement_cache[cache_key]

        result = False

        if orientation == 'horizontal':
            # Check if ship fits on the board horizontally
            if col + size > self.board_size:
                result = False
            else:
                # Check if any cell in the placement has been shot and missed
                valid = True
                for c in range(col, col + size):
                    if self.misses[row, c]:
                        valid = False
                        break
                    # New: also check if we know this is part of another ship
                    if self.hits[row, c]:
                        ship_id = self.ship_hit_map.get((row, c), None)
                        # If it's part of a ship and we know it's not the same orientation
                        if ship_id and any((r, c) for r, c in self.ship_hit_map
                                           if self.ship_hit_map[r, c] == ship_id and r != row):
                            valid = False
                            break
                result = valid
        elif orientation == 'vertical':
            # Check if ship fits on the board vertically
            if row + size > self.board_size:
                result = False
            else:
                # Check if any cell in the placement has been shot and missed
                valid = True
                for r in range(row, row + size):
                    if self.misses[r, col]:
                        valid = False
                        break
                    # New: also check if we know this is part of another ship
                    if self.hits[r, col]:
                        ship_id = self.ship_hit_map.get((r, col), None)
                        # If it's part of a ship and we know it's not the same orientation
                        if ship_id and any((r, c) for r, c in self.ship_hit_map
                                           if self.ship_hit_map[r, c] == ship_id and c != col):
                            valid = False
                            break
                result = valid

        # Store in cache
        self.valid_placement_cache[cache_key] = result
        return result

    def _is_valid_coordinate(self, row, col):
        return (0 <= row < self.board_size and
                0 <= col < self.board_size and
                not self.shots_fired[row, col])

    def _count_valid_placements(self):
        #  Clear cache when board state changes
        self.valid_placement_cache = {}

        # Reset probability map
        self.probability_map = np.zeros((self.board_size, self.board_size))

        # For each remaining ship size
        for ship_size in self.remaining_ships:
            # For each cell on the board
            for r in range(self.board_size):
                for c in range(self.board_size):
                    # Skip cells we've already shot at
                    if self.shots_fired[r, c]:
                        continue

                    # Check horizontal placement
                    if self._can_place_ship(r, c, ship_size, 'horizontal'):
                        for offset in range(ship_size):
                            if c + offset < self.board_size:
                                self.probability_map[r, c + offset] += 1

                    # Check vertical placement
                    if self._can_place_ship(r, c, ship_size, 'vertical'):
                        for offset in range(ship_size):
                            if r + offset < self.board_size:
                                self.probability_map[r + offset, c] += 1

        # Apply heat map to probability map
        self.probability_map *= self.heat_map

        # Modify probability map based on parity in hunt mode
        if self.hunt_mode:
            # Boost cells that match the optimal parity pattern
            self.probability_map *= (1 + 0.75 * self.parity_mask)

    def _get_ship_orientation(self):
        """Determine the orientation of the current ship being targeted."""
        if len(self.current_ship_hits) < 2:
            return None

        # Sort hits by position to ensure consistent detection
        sorted_hits = sorted(self.current_ship_hits)

        # Get the first two hits
        (r1, c1), (r2, c2) = sorted_hits[:2]

        if r1 == r2:  # Same row -> horizontal ship
            return 'horizontal'
        elif c1 == c2:  # Same column -> vertical ship
            return 'vertical'

        # If hits aren't aligned, take the two closest hits
        if len(self.current_ship_hits) > 2:
            # Try to find two hits that are aligned
            for i, (r1, c1) in enumerate(sorted_hits):
                for j, (r2, c2) in enumerate(sorted_hits[i+1:], i+1):
                    if r1 == r2 or c1 == c2:
                        if r1 == r2:
                            return 'horizontal'
                        else:
                            return 'vertical'

        return None  # Unable to determine orientation

    def _generate_target_candidates(self):
        if not self.current_ship_hits:
            return []

        candidates = []

        # If we have multiple hits, determine the ship orientation
        if len(self.current_ship_hits) >= 2:
            self.ship_direction = self._get_ship_orientation()

            if self.ship_direction == 'horizontal':
                # All hits are on the same row
                hit_rows = {hit[0] for hit in self.current_ship_hits}
                if len(hit_rows) == 1:
                    row = next(iter(hit_rows))
                    cols = [hit[1] for hit in self.current_ship_hits]
                    min_col = min(cols)
                    max_col = max(cols)

                    # Check for gaps between min and max
                    for c in range(min_col + 1, max_col):
                        if (row, c) not in self.current_ship_hits and not self.shots_fired[row, c]:
                            # High priority for filling gaps
                            candidates.append((row, c, 15))

                    # Check left side
                    if min_col > 0 and not self.shots_fired[row, min_col - 1]:
                        candidates.append((row, min_col - 1, 10))

                    # Check right side
                    if max_col < self.board_size - 1 and not self.shots_fired[row, max_col + 1]:
                        candidates.append((row, max_col + 1, 10))

            elif self.ship_direction == 'vertical':
                # All hits are on the same column
                hit_cols = {hit[1] for hit in self.current_ship_hits}
                if len(hit_cols) == 1:
                    col = next(iter(hit_cols))
                    rows = [hit[0] for hit in self.current_ship_hits]
                    min_row = min(rows)
                    max_row = max(rows)

                    # Check for gaps between min and max
                    for r in range(min_row + 1, max_row):
                        if (r, col) not in self.current_ship_hits and not self.shots_fired[r, col]:
                            # High priority for filling gaps
                            candidates.append((r, col, 15))

                    # Check top side
                    if min_row > 0 and not self.shots_fired[min_row - 1, col]:
                        candidates.append((min_row - 1, col, 10))

                    # Check bottom side
                    if max_row < self.board_size - 1 and not self.shots_fired[max_row + 1, col]:
                        candidates.append((max_row + 1, col, 10))

        else:  # Only one hit, check all four directions with boundary checking
            row, col = self.current_ship_hits[0]
            # right, down, left, up
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

            for dr, dc in directions:
                r, c = row + dr, col + dc
                if self._is_valid_coordinate(r, c):
                    # Lower priority when direction unknown
                    candidates.append((r, c, 5))

        # Return candidates with their priorities (row, col, priority)
        return candidates if candidates else []

    def _mark_surrounding_cells(self, ship_id):
        # Get all cells of the sunk ship
        ship_coords = [coord for coord,
                       id_val in self.ship_hit_map.items() if id_val == ship_id]

        # Find orientation of the ship
        rows = {r for r, c in ship_coords}
        cols = {c for r, c in ship_coords}

        is_horizontal = len(rows) == 1
        is_vertical = len(cols) == 1

        # Mark surrounding cells as misses
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1)]
        for r, c in ship_coords:
            for dr, dc in directions:
                new_r, new_c = r + dr, c + dc
                if (0 <= new_r < self.board_size and
                    0 <= new_c < self.board_size and
                    not self.shots_fired[new_r, new_c] and
                        (new_r, new_c) not in ship_coords):

                    # Avoid marking cells that could be part of the ship itself
                    is_part_of_ship = False
                    if is_horizontal and new_r == list(rows)[0]:
                        is_part_of_ship = True
                    if is_vertical and new_c == list(cols)[0]:
                        is_part_of_ship = True

                    if not is_part_of_ship:
                        # Mark as missed without actually firing
                        self.misses[new_r, new_c] = True
                        # Add to shots to maintain consistency
                        self.shots_fired[new_r, new_c] = True
                        # Record in game history
                        self.game_history.append(
                            ((new_r, new_c), False, False))

    def update_probability_map(self):
        # Calculate base probabilities from valid ship placements
        self._count_valid_placements()
        # If we're targeting a ship, prioritize those cells
        if not self.hunt_mode:
            self.potential_targets = self._generate_target_candidates()

            # Set probability boost based on priority
            for r, c, priority in self.potential_targets:
                self.probability_map[r, c] *= priority

        # Set probability to 0 for cells already shot at
        self.probability_map[self.shots_fired] = 0
        
        np.set_printoptions(precision=3)
        print(self.probability_map)
        print("next move :", list(np.argwhere(
            self.probability_map == np.max(self.probability_map))))

    def get_move(self, opponent_board=None):
        while self.next_shots:
            next_move = self.next_shots[0]
            if not self.shots_fired[next_move]:
                return self.next_shots.pop(0)
            else:
                # Remove shot if already taken
                self.next_shots.pop(0)

        # If we have potential targets in target mode, use highest probability one
        if not self.hunt_mode and self.potential_targets:
            # Filter out any targets that have already been shot at
            valid_targets = [(r, c, p) for r, c, p in self.potential_targets
                             if not self.shots_fired[r, c]]

            if valid_targets:
                # Sort by priority (third element in tuple)
                valid_targets.sort(key=lambda x: (
                    self.probability_map[x[0], x[1]] * x[2]), reverse=True)
                return valid_targets[0][:2]  # Return just row, col

        # Find all unshot cells
        unshot_mask = ~self.shots_fired

        # If no cells left, return a random position (shouldn't happen in normal game)
        if not np.any(unshot_mask):
            
            # Just to be safe, return any cell that hasn't been recorded as shot
            for r in range(self.board_size):
                for c in range(self.board_size):
                    if not self.shots_fired[r, c]:
                        return (r, c)
            # This should never happen in a normal game
            return (random.randint(0, self.board_size-1), random.randint(0, self.board_size-1))

        # Get probability map for unshot cells only
        masked_probabilities = self.probability_map * unshot_mask

        # Ensure there are valid values
        if np.all(masked_probabilities == 0):
            # If probabilities are all zero, just pick any unshot cell
            coords = np.where(unshot_mask)
            candidates = list(zip(coords[0], coords[1]))
            return random.choice(candidates)

        # Find max probability
        max_prob = np.max(masked_probabilities)

        # Get coordinates of all cells with max probability
        coords = np.where(masked_probabilities == max_prob)
        candidates = list(zip(coords[0], coords[1]))

        # IMPORTANT: Double-check to ensure we're not shooting at already shot cells
        candidates = [(r, c)
                      for r, c in candidates if not self.shots_fired[r, c]]

        if not candidates:
            # Fallback: choose any unshot cell
            coords = np.where(unshot_mask)
            candidates = list(zip(coords[0], coords[1]))

        # Randomly choose among the highest probability cells
        chosen_move = random.choice(candidates)

        # Store this move as the last move to avoid repetition
        self.last_move = chosen_move

        return chosen_move

    def _assign_ship_id(self, row, col):

        # right, down, left, up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        adjacent_ship_ids = set()

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if (0 <= r < self.board_size and
                0 <= c < self.board_size and
                self.hits[r, c] and
                    (r, c) in self.ship_hit_map):
                adjacent_ship_ids.add(self.ship_hit_map[(r, c)])

        if not adjacent_ship_ids:
            # No adjacent hits, assign a new ship ID
            ship_id = self.next_ship_id
            self.next_ship_id += 1
        else:
            # Use the existing ship ID
            ship_id = min(adjacent_ship_ids)

            # Merge ship IDs if there are multiple
            if len(adjacent_ship_ids) > 1:
                for old_id in adjacent_ship_ids:
                    if old_id != ship_id:
                        # Update all coordinates with this old ID
                        for coord, id_val in list(self.ship_hit_map.items()):
                            if id_val == old_id:
                                self.ship_hit_map[coord] = ship_id

        # Assign the ship ID to this coordinate
        self.ship_hit_map[(row, col)] = ship_id
        return ship_id

    def _get_ship_size(self, ship_id):
        return sum(1 for coord, id_val in self.ship_hit_map.items() if id_val == ship_id)

    def _update_ships_after_sink(self, ship_id):
        ship_size = self._get_ship_size(ship_id)
        self.ship_size_map[ship_id] = ship_size

        # Find and remove the appropriate ship size
        if ship_size in self.remaining_ships:
            self.remaining_ships.remove(ship_size)
        else:
            # If exact size not found, remove closest larger size
            larger_sizes = [s for s in self.remaining_ships if s >= ship_size]
            if larger_sizes:
                self.remaining_ships.remove(min(larger_sizes))

    def _reset_targeting(self):
        # Add current ship ID to sunk ships
        if self.current_ship_hits and self.current_ship_hits[0] in self.ship_hit_map:
            ship_id = self.ship_hit_map[self.current_ship_hits[0]]
            self.sunk_ships.add(ship_id)
            self._update_ships_after_sink(ship_id)

            # Mark surrounding cells as misses
            self._mark_surrounding_cells(ship_id)

        # Reset targeting variables
        self.hunt_mode = True
        self.current_ship_hits = []
        self.ship_direction = None
        self.potential_targets = []

    def update_heat_map(self):
        if len(self.game_history) > 5:
            # Analyze hit patterns
            hits = [(r, c) for (r, c), hit, _ in self.game_history if hit]
            if hits:
                # Create a temporary heat map for this update
                temp_heat_map = np.zeros((self.board_size, self.board_size))
                
                # Calculate center of hits
                hit_rows = [r for r, c in hits]
                hit_cols = [c for r, c in hits]
                avg_row = sum(hit_rows) / len(hit_rows)
                avg_col = sum(hit_cols) / len(hit_cols)
                
                # Set Gaussian parameters
                sigma = 2.0  # Controls the spread of influence
                max_influence_radius = 5  # Limit influence to cells within this distance
                
                # Update heat map with Gaussian influence
                for r in range(self.board_size):
                    for c in range(self.board_size):
                        # Calculate Euclidean distance to center of hits
                        dist = ((r - avg_row)**2 + (c - avg_col)**2)**0.5
                        
                        # Only update cells within the influence radius
                        if dist <= max_influence_radius:
                            # Apply Gaussian function for smooth falloff
                            influence = np.exp(-dist**2 / (2 * sigma**2))
                            temp_heat_map[r, c] = influence
                
                # Normalize the temp heat map to have maximum value of 0.2
                # This ensures the update doesn't overwhelm previous learning
                if np.max(temp_heat_map) > 0:
                    temp_heat_map = temp_heat_map * 0.2 / np.max(temp_heat_map)
                
                # Cumulative learning: add to existing heat map rather than resetting
                # Add 1.0 to ensure all cells have at least base probability
                self.heat_map = self.heat_map * 0.9 + temp_heat_map + 1.0
                
                # Ensure the heat map doesn't grow unbounded
                self.heat_map = np.clip(self.heat_map, 1.0, 1.5)

    def notify_result(self, row, col, hit, ship_sunk, game_over):
        
        if self.shots_fired[row, col]:
            # This shot was already recorded, might be a duplicate notification
            return

        # Update basic tracking
        self.shots_fired[row, col] = True

        # Add to game history
        self.game_history.append(((row, col), hit, ship_sunk))

        if hit:
            # Mark as hit
            self.hits[row, col] = True

            # Assign to a ship
#            ship_id = self._assign_ship_id(row, col)

            # Update targeting mode
            self.hunt_mode = False
            if (row, col) not in self.current_ship_hits:
                self.current_ship_hits.append((row, col))

            # If we have multiple hits, determine orientation
            if len(self.current_ship_hits) >= 2:
                self.ship_direction = self._get_ship_orientation()
        else:
            # Mark as miss
            self.misses[row, col] = True

        # Handle ship sinking
        if ship_sunk:
            self._reset_targeting()
            # Update heat map when ship is sunk
            self.update_heat_map()

        # Clear cache because board state changed
        self.valid_placement_cache = {}

        # Filter out any potential targets that are now invalid
        self.potential_targets = [(r, c, p) for r, c, p in self.potential_targets
                                  if not self.shots_fired[r, c]]

        # Update probability map for next move
        self.update_probability_map()

    def reset(self):
        """Reset the AI for a new game."""
        board_size = self.board_size
        ship_sizes = self.ship_sizes.copy()

        # Keep game history for learning
        old_history = self.game_history

        self.__init__(board_size, ship_sizes)

        # Restore game history
        self.game_history = old_history
