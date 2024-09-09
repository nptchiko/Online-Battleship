# Đề tài:
**Online Battleship Game Using Flask-SocketIO in Android**
# Khái quát:
**Battleship là trò chơi nổi tiếng 2 người chơi thể loại board game. Trò chơi được tổ chức trên 1 bảng vuông với 10x10 ô, mỗi ô sẽ đại diện cho tàu hoặc biển. Mỗi người chơi sẽ được 5 con tàu với kích thước 1x1 ô và mục tiêu chính của game là đánh chìm toàn bộ thuyền của đối phương bằng cách đánh bom, người đầu tiên hoàn thành sẽ là người chiến thắng.**

**Trước khi bắt đầu trò chơi, mỗi người chơi sẽ sắp xếp các tàu tùy ý sao cho không có tàu nào trùng ô với nhau, tàu sẽ không thể di chuyển sau khi đặt lên ô. Người chơi chỉ có thấy được vị trị các tàu của bản thân**

**Quy tắc**

+ Mỗi người chơi lần lượt chọn một ô bất kì để thả bom, nếu ô được chọn là tàu thì trò chơi sẽ đánh dấu ô đó là `hit` và người đó được quyền chọn thêm ô mới. Ngược lại, trò chơi sẽ đánh dấu ô đó là `miss` và lượt chơi sẽ dành cho người chơi còn lại.

+ Người chơi không được chọn ô đã được đánh dấu.

![New Project](https://github.com/user-attachments/assets/46fa7fcd-b8e6-4438-9bde-d20e29372605)

# Bài toán đặt ra:
### Vấn đề:
+ Tính năng online nhiều người chơi trong trò chơi

+ Giao diện, thao tác và xử lí các sự kiện trong trò chơi

+ Đồng bộ nội dung trên 2 thiêt bị giữa hai người chơi với nhau

### Đầu vào:
+ Phần lớn thao tác trong trò chơi sẽ là `nhấp`, `thả`, `nhấn` và nên dữ liệu cần quan tâm ở là tọa độ của con trỏ chuột/ngón tay của người màn hình trên màn hình

### Đầu ra:
+ Dựa trên dữ liệu đầu vào, trò chơi sẽ đưa ra các sự kiện khác nhau.

**Ví dụ như:**

+ Nếu tọa độ vượt ra ngoài hitbox(vùng không gian có thể xử lí) thì trò chơi sẽ không phản hồi.
+ Nếu tọa độ người chơi đã chọn là tàu thì trò chơi sẽ thông báo người chơi đã bắn trúng...

### Hướng giải quyết:
+ Trò chơi được xây dựng theo kiến trúc client-server trên giao thức socket để tạo giao tiếp event-base, hai chiều, độ trễ thấp giữa client (Người chơi) và server (Máy chủ)

**Server-side: Flask(python framework), Flask-SocketIO(library supporting Flask)**
+ Trong trò chơi, việc xử lí dự liệu từ client gửi về, quản lí các giao tiếp giữa những người chơi, các phòng chứa người chơi, đảm bảo tính đồng bộ giữa các client với nhau,... được chịu trách nhiệm bới một server(máy chủ). **Flask** và **Flask-SocketIO** sẽ chịu trách nhiệm tạo server.
  
**Client-side: Kotlin(Android programming language)**
+ Thiết kế toàn bộ giao diện của trò chơi, tiếp nhận dữ liệu và các thao tác từ người chơi. Đồng thời tạo client giao tiếp với server với sự hỗ trợ của Socket, lắng nghe phản hồi từ server và trả về dữ liệu cho server. 
# Triển khai ý tưởng: Miku đẹp trai
![image](https://github.com/user-attachments/assets/53ec1e46-8451-4a81-bd91-bf257e8f36ae)

**1. Khởi tạo server và client**

+ Để server có thể hoạt động, bước đầu tiên cần làm là khởi tạo socket cho server, khởi tạo các endpoint để lắng nghe các request từ client.
+ Sau khi khởi tạo xong, ta chạy server trên một port cụ thể và lắng nghe các request từ client.
+ Phía client cũng khởi tạo socket và thực hiện connect với server đang chạy trên port đã biết trước.

**2. Thực hiện 'handshaking'**

+ Client kết nối server:
    + Client thực hiện kết nối với server thông qua Websocket
+ Server thực hiện xác thực kết nối:
    + Server nhận kết nối từ client và yêu cầu xác thực nếu có
    + Server xác nhận kết nối và lưu sessionId của client yêu cầu
    + Server gửi thông điệp về client là kết nối thành công

**3. Quản lí phòng**

+ Client:
    + 

