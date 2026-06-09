import streamlit as st

# 设置网页标题和手机端自适应配置
st.set_page_config(page_title="币浪浪仓位精算器", page_icon="🪙", layout="centered")

# 手机端顶栏样式美化
st.title("🪙 币浪浪仓位精算器")
st.caption("已自动注入万分之四（0.04%）双向手续费控制逻辑")
st.markdown("---")

# 1. 输入区域（手机端会自动变成大字号、易触控的输入框）
entry_price = st.number_input("👉 请输入【当前开仓价格】(U)", min_value=0.0, value=60000.0, step=0.1, format="%.2f")
stop_loss_price = st.number_input("👉 请输入【计划止损价格】(U)", min_value=0.0, value=59400.0, step=0.1, format="%.2f")
max_loss = st.number_input("👉 请输入【你能接受的最大亏损】(U)", min_value=0.0, value=10.0, step=1.0, format="%.2f")

st.markdown("---")

# 2. 核心计算逻辑
fee_rate = 0.0004  # 万四手续费

if entry_price > 0 and stop_loss_price > 0:
    # 计算价格波动百分比
    price_drop_pct = abs(entry_price - stop_loss_price) / entry_price

    if price_drop_pct == 0:
        st.error("❌ 错误：开仓价格和止损价格不能相同！")
    else:
        # 总风险比例 = 波动比例 + 双向手续费
        total_risk_pct = price_drop_pct + (2 * fee_rate)

        # 计算名义仓位
        position_size_usd = max_loss / total_risk_pct
        # 计算币数
        coin_quantity = position_size_usd / entry_price

        # 拆解亏损细节
        estimated_fees = position_size_usd * (2 * fee_rate)
        pure_market_loss = position_size_usd * price_drop_pct

        # 3. 结果渲染（手机端大字号高亮显示，方便复制）
        st.success("📊 【精准计算结果】")

        # 用大指标卡片展示最核心的两个数据
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="🔥 建议开仓总价值", value=f"{position_size_usd:.2f} U")
        with col2:
            st.metric(label="🪙 建议开仓数量", value=f"{coin_quantity:.4f}")

        # 详细数据折叠面板（手机上不占地方）
        with st.expander("🔍 查看亏损和成本细节"):
            st.write(f"• **盘面止损空间:** {price_drop_pct * 100:.3f}%")
            st.write(f"• **双向手续费率:** {2 * fee_rate * 100:.3f}%")
            st.write(f"• **纯市场波动亏损:** {pure_market_loss:.2f} U")
            st.write(f"• **双向手续费损耗:** {estimated_fees:.2f} U")
            st.write(f"• **预计总共亏损:** {pure_market_loss + estimated_fees:.2f} U")
else:
    st.info("💡 请在上方输入正确的价格以激活计算。")