$(document).ready(function () {
    loadIngredients();

    $("#ingredientForm").on("submit", function (event) {
        event.preventDefault();

        const ingredientId = $("#ingredientId").val();

        const data = {
            name: $("#name").val(),
            category: $("#category").val(),
            storage_type: $("#storageType").val(),
            quantity: Number($("#quantity").val()),
            unit: $("#unit").val(),
            expire_date: $("#expireDate").val(),
            memo: $("#memo").val()
        };

        if (ingredientId) {
            updateIngredient(ingredientId, data);
        } else {
            createIngredient(data);
        }
    });

    $("#cancelBtn").on("click", function () {
        resetForm();
    });
});


function loadIngredients() {
    $.ajax({
        url: "/api/ingredients",
        method: "GET",
        success: function (response) {
            renderIngredients(response.data);
        },
        error: function () {
            alert("식재료 목록을 불러오지 못했습니다.");
        }
    });
}


function createIngredient(data) {
    $.ajax({
        url: "/api/ingredients",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function (response) {
            alert(response.message);
            resetForm();
            loadIngredients();
        },
        error: function (xhr) {
            alert(xhr.responseJSON?.message || "등록 실패");
        }
    });
}


function updateIngredient(id, data) {
    $.ajax({
        url: `/api/ingredients/${id}`,
        method: "PUT",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function (response) {
            alert(response.message);
            resetForm();
            loadIngredients();
        },
        error: function () {
            alert("수정 실패");
        }
    });
}


function deleteIngredient(id) {
    if (!confirm("정말 삭제하시겠습니까?")) {
        return;
    }

    $.ajax({
        url: `/api/ingredients/${id}`,
        method: "DELETE",
        success: function (response) {
            alert(response.message);
            loadIngredients();
        },
        error: function () {
            alert("삭제 실패");
        }
    });
}


function consumeIngredient(id) {
    $.ajax({
        url: `/api/ingredients/${id}/consume`,
        method: "PATCH",
        success: function (response) {
            alert(response.message);
            loadIngredients();
        },
        error: function () {
            alert("소비 처리 실패");
        }
    });
}


function editIngredient(item) {
    $("#ingredientId").val(item.id);
    $("#name").val(item.name);
    $("#category").val(item.category);
    $("#storageType").val(item.storage_type);
    $("#quantity").val(item.quantity);
    $("#unit").val(item.unit);
    $("#expireDate").val(item.expire_date);
    $("#memo").val(item.memo);

    $("#formTitle").text("식재료 수정");
    $("#submitBtn").text("수정");

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}


function resetForm() {
    $("#ingredientId").val("");
    $("#ingredientForm")[0].reset();

    $("#formTitle").text("식재료 등록");
    $("#submitBtn").text("등록");
}


function renderIngredients(items) {
    const tbody = $("#ingredientTableBody");
    tbody.empty();

    if (items.length === 0) {
        tbody.append(`
            <tr>
                <td colspan="8">등록된 식재료가 없습니다.</td>
            </tr>
        `);
        return;
    }

    items.forEach(function (item) {
        const status = getStatusText(item.dday);

        const row = `
            <tr>
                <td>${escapeHtml(item.name)}</td>
                <td>${escapeHtml(item.category)}</td>
                <td>${escapeHtml(item.storage_type)}</td>
                <td>${item.quantity} ${escapeHtml(item.unit)}</td>
                <td>${item.expire_date}</td>
                <td>${status}</td>
                <td>${escapeHtml(item.memo || "")}</td>
                <td>
                    <div class="action-buttons">
                        <button class="btn edit-btn"
                                onclick='editIngredient(${JSON.stringify(item)})'>
                            수정
                        </button>

                        <button class="btn consume-btn"
                                onclick="consumeIngredient(${item.id})">
                            소비
                        </button>

                        <button class="btn delete-btn"
                                onclick="deleteIngredient(${item.id})">
                            삭제
                        </button>
                    </div>
                </td>
            </tr>
        `;

        tbody.append(row);
    });
}


function getStatusText(dday) {
    if (dday < 0) {
        return "🔴 만료";
    }

    if (dday === 0) {
        return "🟠 오늘까지";
    }

    if (dday <= 3) {
        return `🟡 D-${dday}`;
    }

    return `🟢 D-${dday}`;
}


function escapeHtml(text) {
    return String(text)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}