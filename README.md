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

### Thuật toán:

+ Trò chơi sẽ chia màn hình thành 1 bảng với 10x10 ô, mỗi ô sẽ có cùng diện tích là 16px và tọa độ khác nhau, ô đầu tiên sẽ bắt đầu với tọa độ (0,0) ở trên bên trái
àn hình
+ Với tọa độ(x,y) đầu vào, ta sẽ tính toán ô tương ứng mà người chơi muốn chọn:
  
      + Nếu x > 160px hoặc y > 160px tức tọa độ hiện tại đã nằm ngoài biên => không phản hồi

      + Cho x = x/16(lấy phần nguyên)
      + Cho y = y/16(lấy phần nguyên)
      + Ta có thể trả về tọa độ ô đang trỏ đến => x,y

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

+ Client yêu câu tham gia phòng:
    
    + Client sẽ lấy số phòng nhập từ người dùng và gửi yêu cầu server để yêu câu tham gia phòng hoặc tạo phòng mới.

+ Server xử lí :

    + Server quản lí các yêu cầu và sắp xếp các client với số phòng.
  
    + Server sẽ kiểm tra:
  
        + Nếu phòng đã tồn tại, thêm client vào phòng đó, và thông báo đến người chơi còn lại và bắt đầu trò chơi

        + Nếu phòng chưa tồn tại thì khởi tạo phòng mới và thêm client vào phòng.

**4. Đồng bộ giữa các client**

+ Client gửi trạng thái:

    + Khi người thao tác thao tác tay nhấp vào màn hình, client sẽ hướng tọa độ và gửi về server tính toán

+ Server đồng bộ client:

    + Server nhận tọa độ do client gửi về và bắt đầu tính toán theo thuật toán đã nêu, cho đầu ra và cập nhật trạng thái game.

    + Server gửi dữ liệu trạng thái mới tới các client trong phòng để đồng bộ hóa nội dung trên toàn bộ client
      
**5. Lối chơi thơì gian thực**

    + Client sẽ nhận dữ liệu trang thái client gửi về và cập nhập giao diện
 
    + Quá trình này sẽ diễn ra liên tục đến khi gặp sự kiện kết thúc
 
**6. Sự kiện kết thúc**

    + Trò chơi sẽ kết thúc một người chơi thỏa điều kiện thắng trước, Server sẽ ghi nhận kết quả và gửi thông báo người chơi, hiển thị `Victory` trên màn hình client người thắng và `Lose` trên client còn lại

    + Server sẽ gửi thông báo đến client liệu có chơi tiếp không

    + Server sẽ xóa đi phòng khi 2 người chơi thoát khỏi phòng

**7. Client đóng kết nối**

    + Khi người chơi muốn rời trò chơi, client sẽ gửi yêu cầu ngắt kết nối đến Server

    + Server nhận request ngắt kết nối, cập nhật lại phòng chơi

    + Server thông báo đến người chơi còn lại khi người chơi thoát phòng
