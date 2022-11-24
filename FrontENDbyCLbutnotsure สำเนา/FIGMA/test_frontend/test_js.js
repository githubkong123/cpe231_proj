
let products = [];

function toShort(str, max = 50) {

    if (str.length > max) {
        return str.substring(0, max) + "....."
    }

    return str;

}

function toShow(x) {
    $("#products").empty();
    x.map(product => {
        $("#products").append(`

            <div class="card product pt-4">
                <img src="${product.image}" class="card-img-top" alt="">
                <div class="card-body border rounded">
                    <p class="card-title font-weight-bold text-nowrap overflow-hidden text-primary">
                    ${product.title}
                    </p>
                    <small class="text-black-50">
                    ${toShort(product.description, 120)}
                    </small>
                    <div class="d-flex justify-content-between align-items-end mt-3">
                        <span class="font-weight-bold">${product.price}</span>
                        <button class="btn btn-sm btn-outline-primary add-to-cart" data-id="${product.id}">
                        Add <i class="fas fa-cart-plus"></i>
                        </button>
                    </div>
                </div>
            </div>

            `)
    })
}

function cartTotal() {

    let count = $(".item-in-cart-cost").length;

    $(".item-in-cart-count").html(count);


    if (count > 0) {
        let totalCost = $(".item-in-cart-cost").toArray().map(el => el.innerHTML).reduce((x, y) => Number(x) + Number(y));
        // console.log(typeof totalCost);
        $(".total").html(`

                <div class="d-flex justify-content-between font-weight-bold px-3">
                    <h4>Total</h4>
                    <h4>$ <span class="cart-cost-total">${Number(totalCost).toFixed(2)}</span></h4>
                </div>
                <div class="d-flex justify-content-between font-weight-bold px-3">   
                </div>
                
                    <div class="modal-footer">
                    
                        
                        <button type="button" class="btn btn-danger" data-dismiss="modal">
                            Buy
                        </button>
                        <!-- Button trigger modal -->
                        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
                            Buy
                        </button>

                        <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                            <div class="modal-dialog">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                    </div>
                                    <div class="modal-body">
                                        ...
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                        <button type="button" class="btn btn-primary">Save changes</button>
                                    </div>
                                </div>
                            </div>
                        </div>



                    
                    </div>
                

            `)


    } else {
        $(".total").html("empty cart")
    }







}

function cartbuy() {
    let count = $(".item-in-cart-cost").length;

    $(".item-in-cart-count").html(count);

    if (count > 0) { }







}









$.get("https://fakestoreapi.com/products/", function (data) {
    products = data;
    toShow(products);
})

$("#search").on("keyup", function () {
    let keyword = $(this).val().toLowerCase();
    // $(".product").filter(function () {
    //
    //     $(this).toggle($(this).text().toLowerCase().indexOf(keyword) > -1);
    //
    // });

    console.log();

    if (keyword.trim().length) {

        let filterProducts = products.filter(product => {
            if (product.title.toLowerCase().indexOf(keyword) > -1 || product.description.toLowerCase().indexOf(keyword) > -1 || product.price == keyword) {
                return product;
            }
        })

        toShow(filterProducts);
    }

});

$.get("https://fakestoreapi.com/products/categories", function (data) {
    data.map(cat => $("#category").append(`<option value="${cat}">${cat}</option>`))
})

$("#category").on("change", function () {

    let selectedCategory = $(this).val();
    console.log(typeof selectedCategory);

    if (selectedCategory != 0) {
        let filterProducts = products.filter(product => {
            if (product.category === selectedCategory) {
                return product;
            }
        })

        toShow(filterProducts);
    } else {
        toShow(products);
    }
})



$("#products").delegate(".add-to-cart", "click", function () {
    let currentItemId = $(this).attr("data-id");

    let productInfo = products.filter(el => el.id == currentItemId)[0];

    // if($(".item-in-cart").toArray().map(el=>el.getAttribute("data-id")).includes(currentItemId)){

    //     alert("Already Added")

    // }else{

    $("#cart").append(`
        <div class="card border-0 item-in-cart" data-id="${productInfo.id}">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-end">
                    <img src="${productInfo.image}" class="img-in-cart" alt="">
                    <button class="btn btn-outline-danger remove-from-cart">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
                <p class="mt-3">
                    ${productInfo.title}
                </p>

                <div class="d-flex justify-content-between align-items-end">
                    <div class="form-row">
                        <button class="btn btn-outline-primary quantity-minus">
                            <i class="fas fa-minus"></i>
                        </button>
                        <input type="number" class="form-control w-25 mx-2 quantity" unitPrice="${productInfo.price}" value="1" min="1">
                        <button class="btn btn-outline-primary quantity-plus">
                            <i class="fas fa-plus"></i>
                        </button>
                    </div>
                    
                    <p class="mb-0">$ <span class="item-in-cart-cost">${(productInfo.price)}</span></p>
                </div>

                <hr>
            </div>
        </div>
        `);

    // }

    cartTotal();

})

$("#cart").delegate(".remove-from-cart", "click", function () {

    $(this).parentsUntil("#cart").remove();
    cartTotal();

})

$("#cart").delegate(".remove-from-cart", "click", function () {

    $(this).parentsUntil("#cart").remove();
    cartTotal();

})





$("#cart").delegate(".quantity-plus", "click", function () {

    let q = $(this).siblings(".quantity").val();
    let p = $(this).siblings(".quantity").attr("unitPrice");
    let newQ = Number(q) + 1;
    let newCost = p * newQ;
    // console.log(p);
    $(this).siblings(".quantity").val(newQ);
    $(this).parent().siblings("p").find(".item-in-cart-cost").html(newCost.toFixed(2));
    cartTotal();
})


$("#cart").delegate(".quantity-minus", "click", function () {

    let q = $(this).siblings(".quantity").val();
    let p = $(this).siblings(".quantity").attr("unitPrice");
    if (q > 1) {

        let newQ = Number(q) - 1;
        let newCost = p * newQ;
        console.log(q);
        console.log(p);
        $(this).siblings(".quantity").val(newQ);
        $(this).parent().siblings("p").find(".item-in-cart-cost").html(newCost.toFixed(2));
        cartTotal();

    }

})

// function quantity_size() { 

//     return $('#mySelect option:selected').val()
// }

// $("#cart").delegate(".quantity-size","click",function () {


//     let p = $(this).siblings(".quantity").attr("unitPrice");
//     let x = $('#mySelect :selected').val();

//     let newCost = p + x;
//     console.log(x);
//     $(this).parent().siblings("p").find(".item-in-cart-cost").html(newCost.toFixed(2));
//     cartTotal();

// })



$("#cart").delegate(".quantity", "keyup change", function () {

    let q = $(this).val();
    let p = $(this).attr("unitPrice");

    if (q > 1) {

        let newQ = Number(q);

        let newCost = p * newQ;
        // console.log(p);
        $(this).val(newQ);
        $(this).parent().siblings("p").find(".item-in-cart-cost").html(newCost.toFixed(2));
        cartTotal();

    } else {
        alert("more than one");
    }

})

