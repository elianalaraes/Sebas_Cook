document.addEventListener('DOMContentLoaded', () => {
    const receiptList = document.getElementById('receipt-list');
    const receiptTotal = document.getElementById('receipt-total');

    const selections = {};

    // Función para mostrar alertas en lugar del alert() nativo del navegador
    function showFlashMessage(message, category = 'danger') {
        const flashContainer = document.querySelector('.flash-messages');
        if (!flashContainer) return;

        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${category}`;
        alertDiv.textContent = message;

        flashContainer.appendChild(alertDiv);

        // Auto-eliminar la alerta tras 4 segundos
        setTimeout(() => {
            alertDiv.style.transition = "all 0.4s ease";
            alertDiv.style.opacity = "0";
            alertDiv.style.transform = "translateY(-10px) scale(0.9)";
            setTimeout(() => alertDiv.remove(), 400);
        }, 4000);
    }

    // 1. Manejo de botones de variante/sabor
    document.querySelectorAll('.pill-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            if (e.target.hasAttribute('disabled') || e.target.getAttribute('data-sold-out') === 'true') {
                return;
            }

            const card = e.target.closest('.card');
            card.querySelectorAll('.pill-btn').forEach(btn => btn.classList.remove('active'));
            e.target.classList.add('active');

            const priceBadge = card.querySelector('.price-badge');
            if (priceBadge) {
                const newPrice = e.target.getAttribute('data-price');
                priceBadge.setAttribute('data-price', newPrice);
                priceBadge.textContent = `${Math.round(newPrice)}$`;
            }

            const activeKey = getActiveVariantKey(card);
            const currentCount = selections[activeKey] ? selections[activeKey].count : 0;
            card.querySelector('.count-val').textContent = currentCount;
        });
    });

    // 2. Manejo de + y - con bloqueo estricto
    document.querySelectorAll('.card').forEach(card => {
        const plusBtn = card.querySelector('.btn-plus');
        const minusBtn = card.querySelector('.btn-minus');
        const countVal = card.querySelector('.count-val');
        const status = card.getAttribute('data-item-status');

        // Verificar si el producto general no está disponible
        const isProductDisabled = ['seasonal', 'temporada', 'sold_out', 'agotado'].includes(status);

        if (plusBtn && minusBtn) {
            plusBtn.addEventListener('click', () => {
                // Si el producto completo está bloqueado
                if (isProductDisabled || plusBtn.hasAttribute('disabled')) {
                    return;
                }

                // Verificar si la variante/sabor seleccionado está deshabilitado
                const activePill = card.querySelector('.pill-btn.active');
                if (!activePill) {
                    showFlashMessage("Por favor, selecciona un sabor primero.", "danger");
                    return;
                }
                if (activePill && (activePill.hasAttribute('disabled') || activePill.getAttribute('data-sold-out') === 'true')) {
                    return;
                }

                const key = getActiveVariantKey(card);
                const info = getActiveVariantInfo(card);

                if (!selections[key]) {
                    selections[key] = { ...info, count: 0 };
                }

                const remaining = parseInt(activePill.dataset.remaining);

                if (selections[key].count >= remaining) {
                    showFlashMessage(`Solo quedan ${remaining} disponibles de este sabor.`, "danger");
                    return;
                }

                selections[key].count += 1;
                countVal.textContent = selections[key].count;
                updateReceipt();
            });

            minusBtn.addEventListener('click', () => {
                if (isProductDisabled || minusBtn.hasAttribute('disabled')) {
                    return;
                }

                const key = getActiveVariantKey(card);

                if (selections[key] && selections[key].count > 0) {
                    selections[key].count -= 1;
                    countVal.textContent = selections[key].count;

                    if (selections[key].count === 0) {
                        delete selections[key];
                    }
                    updateReceipt();
                }
            });
        }
    });

    function getActiveVariantKey(card) {
        const itemId = card.getAttribute('data-item-id');
        const activePill = card.querySelector('.pill-btn.active');

        if (!activePill) {
            return null;
        }

        return `${itemId}_${activePill.getAttribute('data-variant-name')}`;
    }

    function getActiveVariantInfo(card) {
        const productName = card.querySelector('.product-name').textContent.trim();
        const activePill = card.querySelector('.pill-btn.active');

        let variantName = activePill ? activePill.getAttribute('data-variant-name') : '';
        let price = activePill ? parseFloat(activePill.getAttribute('data-price')) : 0;

        if (!activePill && card.querySelector('.price-badge')) {
            price = parseFloat(card.querySelector('.price-badge').getAttribute('data-price'));
        }

        return { productName, variantName, price };
    }

    function updateReceipt() {
        receiptList.innerHTML = '';
        let total = 0;

        Object.values(selections).forEach(item => {
            if (item.count > 0) {
                const subtotal = item.price * item.count;
                total += subtotal;

                const displayName = item.variantName && item.variantName !== 'Estándar' && item.variantName !== 'Tradicional' && item.variantName !== 'Standard'
                    ? `${item.productName} (${item.variantName}) x${item.count}`
                    : `${item.productName} x${item.count}`;

                const row = document.createElement('div');
                row.className = 'receipt-row';
                row.innerHTML = `<span>${displayName}</span><span>$${subtotal}</span>`;
                receiptList.appendChild(row);
            }
        });

        document.getElementById('order-items').value =
        JSON.stringify(Object.values(selections));

        receiptTotal.textContent = `$${total}`;
    }
});