$(document).ready(function() {
    // Tính toán và cập nhật tổng tiền khi địa chỉ thay đổi
    function updateShippingFee() {
        const subtotal = parseFloat($('#subtotal').text().replace(/[^0-9]/g, '')) || 0;
        const province = $('#province').val();
        const district = $('#district').val();
        const ward = $('#ward').val();
        
        if (!province) {
            // Nếu chưa chọn tỉnh thành, không cập nhật
            return;
        }
        
        // Hiển thị loading
        $('#shipping-fee').html('<span class="text-muted">Đang tính...</span>');
        $('#grand-total').html('<span class="text-muted">Đang tính...</span>');
        
        // Gọi API để tính phí ship
        $.ajax({
            url: '/api/calculate-shipping',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                subtotal: subtotal,
                province: province,
                district: district,
                ward: ward
            }),
            success: function(response) {
                if (response.success) {
                    const shippingFee = response.shipping_fee;
                    const grandTotal = subtotal + shippingFee;
                    
                    // Cập nhật hiển thị
                    $('#shipping-fee').text(formatCurrency(shippingFee));
                    $('#grand-total').text(formatCurrency(grandTotal));
                    
                    // Hiển thị thông tin phương thức vận chuyển
                    if (response.is_free) {
                        $('#shipping-info').html('<small class="text-success">🎉 Miễn phí vận chuyển!</small>');
                    } else if (response.selected_rate) {
                        const rate = response.selected_rate;
                        let info = `<small class="text-muted">${rate.shipping_method}`;
                        if (rate.estimated_delivery_days) {
                            info += ` - ${rate.estimated_delivery_days} ngày`;
                        }
                        info += '</small>';
                        $('#shipping-info').html(info);
                    }
                } else {
                    // Xử lý lỗi
                    const fallbackFee = response.shipping_fee || 50000;
                    const grandTotal = subtotal + fallbackFee;
                    
                    $('#shipping-fee').text(formatCurrency(fallbackFee));
                    $('#grand-total').text(formatCurrency(grandTotal));
                    $('#shipping-info').html('<small class="text-warning">Lỗi tính phí ship, dùng giá mặc định</small>');
                }
            },
            error: function() {
                // Xử lý lỗi network
                const fallbackFee = 50000;
                const grandTotal = subtotal + fallbackFee;
                
                $('#shipping-fee').text(formatCurrency(fallbackFee));
                $('#grand-total').text(formatCurrency(grandTotal));
                $('#shipping-info').html('<small class="text-danger">Không thể tính phí ship, dùng giá mặc định</small>');
            }
        });
    }
    
    // Format số tiền
    function formatCurrency(amount) {
        return new Intl.NumberFormat('vi-VN', {
            style: 'currency',
            currency: 'VND'
        }).format(amount);
    }
    
    // Lắng nghe sự kiện thay đổi địa chỉ
    $('#province, #district, #ward').on('change', function() {
        updateShippingFee();
    });
    
    // Khởi tạo tính phí ship ban đầu
    updateShippingFee();
});