# Đề tài:
**Online Battleship Game Using Flask-SocketIO in Android**
# Khái quát:
**-> Battleship là trò chơi nổi tiếng 2 người chơi thể loại board game. Trò chơi được tổ chức trên 1 bảng vuông với 10x10 ô, mỗi ô sẽ đại diện cho tàu hoặc biển. Mỗi người chơi sẽ được 5 con tàu với kích thước 1x1 ô và mục tiêu chính của game là đánh chìm toàn bộ thuyền của đối phương bằng cách đánh bom, người đầu tiên hoàn thành sẽ là người chiến thắng.**

**-> Trước khi bắt đầu trò chơi, mỗi người chơi sẽ sắp xếp các tàu tùy ý sao cho không có tàu nào trùng ô với nhau, tàu sẽ không thể di chuyển sau khi đặt lên ô. Người chơi chỉ có thấy được vị trị các tàu của bản thân**

**-> Quy tắc:**

**+ Mỗi người chơi lần lượt chọn một ô bất kì để thả bom, nếu ô được chọn là tàu thì trò chơi sẽ đánh dấu ô đó là `hit` và người đó được quyền chọn thêm ô mới. Ngược lại, trò chơi sẽ đánh dấu ô đó là `miss` và lượt chơi sẽ dành cho người chơi còn lại.**

**+ Người chơi không được chọn ô đã được đánh dấu.**

![New Project](https://github.com/user-attachments/assets/46fa7fcd-b8e6-4438-9bde-d20e29372605)

# Bài toán đặt ra:
### Công nghệ áp dụng:
  **+ Server-side: Python, Flask-SocketIO, Flask framework**

  **+ Client-side: Kotlin**
