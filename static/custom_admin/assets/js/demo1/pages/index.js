

function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      $('#bp_img').attr('src', e.target.result);
    }

    reader.readAsDataURL(input.files[0]);
  }
}

$("#image_uri").change(function() {
  readURL(this);
});

$("#logoUri").change(function() {
  readURL(this);
});

$("#avatar").change(function() {
  readURL(this);
});



$('.delete_confirm_swta').click(function(e) {
    e.preventDefault();
     var link = $(this).attr('href');
    swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        type: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'No, cancel!',
        reverseButtons: true
    }).then(function(result){
        if (result.value) {
            window.location.href = link;

        } else if (result.dismiss === 'cancel') {
            swal.fire(
                'Cancelled',
                'Blog post has not deleted.',
                'error'
            )
        }
    });
});


// Begin :: Ajax



// End :: Ajax