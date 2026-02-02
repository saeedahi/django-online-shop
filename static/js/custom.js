function showLargeImage(imageSrc) {
    console.log(imageSrc);
    $('#main_image').attr('src', imageSrc);
    $('#show-large-image').attr('href', imageSrc);
}

function addComment(productId) {
    var comment = $('#commentText').val();
    var parentId = $('#parent_id').val();

    $.ajax({
        url: '/products/add-comment/',
        type: 'POST',
        data: {
            comment: comment,
            product_id: productId,
            parent_id: parentId,
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
        },
        success: function(res) {
            $('#two').html(res);
            $('#commentText').val('');    // پاک کردن textarea بعد از ارسال
            $('#parent_id').val('');
        },
        error: function(err) {
            console.log(err.responseJSON);
            alert('خطا در ارسال نظر');
        }
    })

    // $.get('/products/add-comment/', {
    //     product_comment: comment,
    //     product_id: productId,
    //     parent_id: parentId
    // }).then(res => {
    //     // console.log(res);
    //     $('#two').html(res);
    // });
}

function fillParentId(parentId) {
    $('#parent_id').val(parentId);
    document.getElementById('comment_form').scrollIntoView({behavior: 'smooth'});
}

// function searchProducts() {
//     event.preventDefault();
//     var text = $('#searchbar').val();
//     console.log(text);
//     $.get('', {
//         search_text: text,
//     });
// }