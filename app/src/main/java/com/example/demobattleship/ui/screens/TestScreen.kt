import android.content.Context
import android.content.pm.ActivityInfo
import androidx.compose.foundation.*
import androidx.compose.foundation.gestures.Orientation
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.draggable
import androidx.compose.foundation.gestures.rememberDraggableState
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.demobattleship.MainActivity
import com.example.demobattleship.ui.theme.DemoBattleShipTheme
import kotlin.math.roundToInt

@Composable
fun ChessBoard(draggedPiece: MutableState<Offset?>) {
    LazyVerticalGrid(
        columns = GridCells.Fixed(10),
        modifier = Modifier.fillMaxSize()
    ) {
        items(100) { index ->
            Box(
                modifier = Modifier
                    .size(30.dp)
                    .pointerInput(Unit) {
                        detectDragGestures { change, dragAmount ->
                            // Xử lý kéo thả vào bàn cờ ở đây
                        }
                    }
            ) {
                if (draggedPiece.value != null) {
                    // Hiển thị quân cờ đang được kéo
                    Box(
                        modifier = Modifier
                            .size(30.dp)
                            .offset {
                                IntOffset(
                                    draggedPiece.value?.x?.roundToInt() ?: 0,
                                    draggedPiece.value?.y?.roundToInt() ?: 0
                                )
                            }
                            .background(Color.Red)
                    )
                }
                Text(text = "$index")
            }
        }
    }
}

@Composable
fun PieceColumn(draggedPiece: MutableState<Offset?>) {
    Column {
        repeat(5) { index ->
            Box(
                modifier = Modifier
                    .size(30.dp)
                    .pointerInput(Unit) {
                        detectDragGestures(
                            onDragStart = {
                                draggedPiece.value = Offset.Zero
                            },
                            onDragEnd = {
                                draggedPiece.value = null
                            }
                        ) { change, dragAmount ->
                            change.consume()
                            draggedPiece.value = draggedPiece.value?.plus(dragAmount)
                        }
                    }
                    .background(Color.Gray)
            ) {
                Text(text = "Piece $index")
            }
        }
    }
}

@Composable
fun DragAndDropBoard() {
    val draggedPiece = remember { mutableStateOf<Offset?>(null) }

    Row {
        PieceColumn(draggedPiece)
        ChessBoard(draggedPiece)
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun App() {
    MaterialTheme {
        DragAndDropBoard()
    }
}

@Composable
fun TestScreen(context: Context) {
    (context as MainActivity)?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE
    Scaffold { paddingValues ->
        Column(modifier = Modifier.padding(paddingValues)) {
            DragAndDropBoard()
        }
    }
}


@Preview(showBackground = true, device = "spec:width=712dp,height=360dp,orientation=landscape")
@Composable
fun Hah() {
    DemoBattleShipTheme {
//        BoardScreen(board = DataResource().loadBoard())
//        HomeScreen(context = LocalContext.current)
        TestScreen(context = LocalContext.current)
    }
}