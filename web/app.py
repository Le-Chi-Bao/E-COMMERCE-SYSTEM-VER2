import sys
import os

# Thêm parent directory vào Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import sau khi đã thêm path
from services.ecommerce_service import ecommerce
import gradio as gr

def create_app():
    # Sử dụng theme đẹp hơn
    with gr.Blocks(
        title="Hệ Thống Dự Đoán Điện Thoại",
        theme=gr.themes.Default(
            primary_hue="violet", 
            secondary_hue="emerald",
            font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"],
            spacing_size="lg",
            radius_size="lg"
        )
        # theme=gr.themes.Base(
        #     primary_hue="blue",
        #     secondary_hue="slate",
        #     font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui"],
        #     spacing_size="md",
        #     radius_size="lg"
        # )    
        # theme=gr.themes.Soft(
        #     primary_hue="blue",
        #     secondary_hue="slate",
        #     font=[gr.themes.GoogleFont("Poppins"), "Arial", "sans-serif"],
        #     spacing_size="md",
        #     radius_size="lg"
        # )
    ) as demo:
        
        gr.Markdown("""
        # MINI E-COMMERCE SYSTEM
        *Hệ thống mua sắm trực tuyến*
        """)
        
        # ========== AUTHENTICATION SECTION ==========
        with gr.Tab("Tài khoản"):    
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Đăng nhập")
                    login_username = gr.Textbox(label="Tên đăng nhập")
                    login_password = gr.Textbox(label="Mật khẩu", type="password")
                    login_btn = gr.Button("Đăng nhập", variant="primary")
                    login_status = gr.Textbox(label="Trạng thái", interactive=False)
                    
                    current_user_display = gr.Textbox(
                        label="Người dùng hiện tại", 
                        value="Chưa đăng nhập",
                        interactive=False
                    )
                    logout_btn = gr.Button("Đăng xuất")
                
                with gr.Column():
                    gr.Markdown("### Đăng ký tài khoản mới")
                    reg_username = gr.Textbox(label="Tên đăng nhập")
                    reg_email = gr.Textbox(label="Email")
                    reg_password = gr.Textbox(label="Mật khẩu", type="password")
                    register_btn = gr.Button("Đăng ký", variant="secondary")
                    register_status = gr.Textbox(label="Trạng thái", interactive=False)
        
        # ========== PRODUCTS SECTION ==========
        with gr.Tab("Sản phẩm"):
            with gr.Row():
                category_dropdown = gr.Dropdown(
                    label="Lọc theo danh mục",
                    choices=ecommerce.get_categories(),
                    value="Tất cả"
                )
            
            products_output = gr.JSON(label="Danh sách sản phẩm")
            
            with gr.Row():
                product_id_input = gr.Number(label="Mã sản phẩm", precision=0)
                quantity_input = gr.Number(label="Số lượng", value=1, precision=0)
                add_to_cart_btn = gr.Button("Thêm vào giỏ hàng", variant="primary")
            
            add_to_cart_status = gr.Textbox(label="Thông báo", interactive=False)
        
        # ========== CART SECTION ==========
        with gr.Tab("Giỏ hàng"):
            cart_output = gr.JSON(label="Sản phẩm trong giỏ hàng")
            cart_total = gr.Textbox(label="Tổng tiền", interactive=False)
            
            with gr.Row():
                refresh_cart_btn = gr.Button("Làm mới giỏ hàng")
                clear_cart_btn = gr.Button("Xóa giỏ hàng", variant="stop")
            
            checkout_btn = gr.Button("Thanh toán", variant="primary")
            checkout_status = gr.Textbox(label="Trạng thái thanh toán", interactive=False)
        
        # ========== ORDERS SECTION ==========
        with gr.Tab("Đơn hàng"):
            orders_output = gr.JSON(label="Lịch sử đơn hàng")
            refresh_orders_btn = gr.Button("Làm mới danh sách đơn hàng")
        
        # ========== ADMIN DASHBOARD SECTION ==========
        with gr.Tab("Quản trị"):
                    gr.Markdown("### 🎛️ Quản trị hệ thống")
                    admin_status = gr.Textbox(label="Trạng thái", value="Chưa đăng nhập với quyền Admin", interactive=False)
                    
                    # Sử dụng Tabs để tổ chức admin section
                    with gr.Tabs():
                        with gr.TabItem(" Người dùng"):
                            with gr.Column():
                                gr.Markdown("#### Quản lý Người dùng")
                                admin_users_output = gr.JSON(label="Danh sách người dùng")
                                refresh_users_btn = gr.Button("Làm mới danh sách người dùng")
                        
                        with gr.TabItem(" Sản phẩm"):
                            with gr.Column():
                                gr.Markdown("#### Quản lý Sản phẩm")
                                admin_products_output = gr.JSON(label="Danh sách sản phẩm")
                                refresh_products_btn = gr.Button("Làm mới danh sách sản phẩm")
                        
                        with gr.TabItem(" Đơn hàng"):
                            with gr.Column():
                                gr.Markdown("#### Quản lý Đơn hàng")
                                admin_orders_output = gr.JSON(label="Tất cả đơn hàng")
                                refresh_admin_orders_btn = gr.Button("Làm mới danh sách đơn hàng")
                        
                        with gr.TabItem(" Báo cáo"):
                            with gr.Column():
                                gr.Markdown("#### Báo cáo & Thống kê")
                                sales_report = gr.JSON(label="Báo cáo doanh thu")
                                generate_report_btn = gr.Button("Tạo báo cáo")
        
        # ========== EVENT HANDLERS ==========
        def handle_login(username, password):
            result = ecommerce.login_user(username, password)
            user_display = f"{username}" if "thành công" in result else "Chưa đăng nhập"
            
            # Cập nhật trạng thái admin
            admin_status_value = "Đã đăng nhập với quyền Admin" if username == "admin" else "Đã đăng nhập User thường"
            return result, user_display, admin_status_value
        
        def handle_logout():
            result = ecommerce.logout_user()
            return result, "Chưa đăng nhập", "Chưa đăng nhập Admin"
        
        login_btn.click(
            fn=handle_login,
            inputs=[login_username, login_password],
            outputs=[login_status, current_user_display, admin_status]
        ).then(
            fn=lambda: ecommerce.get_products(),
            outputs=products_output
        )
        
        logout_btn.click(
            fn=handle_logout,
            outputs=[login_status, current_user_display, admin_status]
        ).then(
            fn=lambda: ecommerce.get_products(),
            outputs=products_output
        ).then(
            fn=lambda: ([], "0₫"),
            outputs=[cart_output, cart_total]
        )
        
        register_btn.click(
            fn=ecommerce.register_user,
            inputs=[reg_username, reg_email, reg_password],
            outputs=register_status
        )
        
        category_dropdown.change(
            fn=lambda cat: ecommerce.get_products(cat),
            inputs=category_dropdown,
            outputs=products_output
        )
        
        add_to_cart_btn.click(
            fn=ecommerce.add_to_cart,
            inputs=[product_id_input, quantity_input],
            outputs=add_to_cart_status
        )
        
        def display_cart():
            cart_items = ecommerce.get_cart_items()
            total = ecommerce.get_cart_total()
            return cart_items, f"{total:,.0f}₫"
        
        refresh_cart_btn.click(
            fn=display_cart,
            outputs=[cart_output, cart_total]
        )
        
        clear_cart_btn.click(
            fn=ecommerce.clear_cart,
            outputs=[checkout_status]
        ).then(
            fn=display_cart,
            outputs=[cart_output, cart_total]
        )
        
        checkout_btn.click(
            fn=ecommerce.checkout,
            outputs=checkout_status
        ).then(
            fn=display_cart,
            outputs=[cart_output, cart_total]
        )
        
        refresh_orders_btn.click(
            fn=ecommerce.get_user_orders,
            outputs=orders_output
        )
        
        # ========== ADMIN EVENT HANDLERS ==========
        refresh_users_btn.click(
            fn=ecommerce.get_all_users,
            outputs=admin_users_output
        )
        
        refresh_products_btn.click(
            fn=ecommerce.get_all_products,
            outputs=admin_products_output
        )
        
        refresh_admin_orders_btn.click(
            fn=ecommerce.get_all_orders,
            outputs=admin_orders_output
        )
        
        generate_report_btn.click(
            fn=ecommerce.get_sales_analytics,
            outputs=sales_report
        )
        
        # Load initial data
        demo.load(
            fn=lambda: ecommerce.get_products(),
            outputs=products_output
        )
        
        demo.load(
            fn=display_cart,
            outputs=[cart_output, cart_total]
        )
        
        demo.load(
            fn=ecommerce.get_user_orders,
            outputs=orders_output
        )
    
    return demo

if __name__ == "__main__":
    print("🚀 Khởi chạy Mini E-commerce System...")
    app = create_app()
    app.launch(
        server_name="0.0.0.0",  
        server_port=8866,
        share=False
    )