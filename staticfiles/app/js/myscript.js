console.log("myscript loaded");

$('.plus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];

    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id
        },
        success: function (data) {
            eml.innerText = data.quantity;
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
        }
    });
});


$('.minus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];

    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function (data) {
            eml.innerText = data.quantity;
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
        }
    });
});

$('.remove-cart').click(function () {

    var id = $(this).attr("pid").toString();
    var eml = this;

    $.ajax({
        type: "GET",
        url: "/removecart/",
        data: {
            prod_id: id
        },

        success: function (data) {

            eml.parentNode.parentNode.parentNode.parentNode.remove();

            document.getElementById("amount").innerText =
                "Rs. " + data.amount;

            document.getElementById("totalamount").innerText =
                "Rs. " + data.totalamount;
        }
    });
});




$('.plus-wishlist').click(function () {
    var id = $(this).attr("pid").toString();

    $.ajax({
        type: "GET",
        url: "/pluswishlist",
        data: {
            prod_id: id
        },
        success: function (data) {
            location.reload();
        }
    });
});

$('.minus-wishlist').click(function () {
    var id = $(this).attr("pid").toString();

    $.ajax({
        type: "GET",
        url: "/minuswishlist",
        data: {
            prod_id: id
        },
        success: function (data) {
            location.reload();
        }
    });
});