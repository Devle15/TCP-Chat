# TCP-Chat

## Giới thiệu
TCP-Chat là ứng dụng chat client–server sử dụng giao thức TCP Socket,
được xây dựng bằng C# (.NET).
Hệ thống cho phép nhiều client kết nối đến server để gửi/nhận tin nhắn
và gửi file trong mạng nội bộ.

## Công nghệ sử dụng
- Ngôn ngữ: C#
- Nền tảng: .NET 8
- Mô hình: Client – Server
- Giao thức: TCP Socket
- Giao diện: Windows Forms

## Chức năng chính
- Server:
  - Lắng nghe kết nối từ nhiều client
  - Quản lý danh sách client đang kết nối
  - Nhận và broadcast tin nhắn
  - Ghi log hoạt động

- Client:
  - Kết nối tới server
  - Gửi và nhận tin nhắn
  - Gửi file cho các client khác
  - Hiển thị lịch sử chat

## Cách chạy chương trình

### 1. Yêu cầu
- Windows
- .NET SDK 8.0 trở lên

### 2. Chạy Server
1. Mở project bằng Visual Studio hoặc VS Code
2. Chạy project `ChatServer`
3. Server sẽ lắng nghe tại cổng `5000`

### 3. Chạy Client
1. Chạy project `ChatClient`
2. Nhập tên người dùng
3. Nhấn **Kết nối**
4. Bắt đầu chat

## Ghi chú
- Chạy nhiều client để test chat nhiều người
- Server và client có thể chạy trên các máy khác nhau trong cùng mạng LAN
