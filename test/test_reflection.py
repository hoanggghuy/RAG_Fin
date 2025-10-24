from reflection.reflection import Reflection
reflection = Reflection()
text =  [
    {
      "role": "user",
      "content": "Samsung Galaxy Z Fold7 dùng chip gì ?"
    },
    {
      "role": "assistant",
      "content": "Chào anh/chị — trả lời ngắn gọn như chuyên gia tư vấn:\n\n- Samsung Galaxy Z Fold7 không dùng Exynos mà dùng chip Snapdragon.  \n- Cụ thể (theo thông tin sản phẩm): chip là \"Snapdragon 8 Elite for Galaxy\" (tiến trình 3 nm).  \n- Theo mô tả sản phẩm, cả phiên bản bán ở Việt Nam và bản quốc tế đều trang bị chipset này (không phải Exynos).\n\nLợi ích thực tế: Snapdragon 8 Elite for Galaxy mạnh mẽ và tiết kiệm điện hơn so với chip trên Fold6 (được nhắc đến là Snapdragon 8 Gen 3 4nm), giúp xử lý đa nhiệm, game nặng và các tác vụ AI mượt hơn, đồng thời tối ưu hóa thời lượng pin. Máy mẫu bạn đang quan tâm có cấu hình 12GB/512GB và pin 4400 mAh.\n\nNếu anh/chị muốn, tôi có thể so sánh hiệu năng thực tế giữa Fold7 và Fold6 hoặc tư vấn mẫu tương đương phù hợp với nhu cầu (game, sáng tạo nội dung, hay làm việc)."
    },
    {
      "role": "user",
      "content": "Điện thoại này giá bao nhiêu ?"
    },
    {
      "role": "assistant",
      "content": "Chào anh/chị, cảm ơn đã quan tâm!\n\nGiá Samsung Galaxy Z Fold7 bên em hiện tại như sau:\n- 12GB/256GB: 42.990.000 ₫  \n- 12GB/512GB: 46.990.000 ₫\n\nMàu sắc (hiện có tại cửa hàng) và giá:\n- Xanh Navy: 46.990.000 ₫  \n- Đen Tuyền: 46.990.000 ₫  \n- Xám Bạc: 46.990.000 ₫\n\nLưu ý: các màu đang niêm yết với mức giá 46.990.000 ₫ (tương ứng với bản 12GB/512GB).  \nSamsung Galaxy Z Fold7 đã có mặt tại Hoàng Hà Mobile với mức giá hấp dẫn. Nếu anh/chị cần kiểm tra tồn kho, đặt mua, hoặc hỗ trợ trả góp/đổi cũ lấy mới, vui lòng gọi tổng đài 1900 2091 — đội ngũ tư vấn của Hoàng Hà Mobile sẵn sàng hỗ trợ. Anh/chị muốn mình kiểm tra thêm thông tin nào không?"
    }
  ]

print(reflection.concat_and_format_text(text))