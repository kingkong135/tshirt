window.addEventListener('DOMContentLoaded', function () {
    // const avatar = document.getElementById('avatar');
    const image = document.getElementById('image');
    const input = document.getElementById('input');
    const $alert = $('.alert');
    const $modal = $('#modal');
    let cropper;

    btnSave.hide();

    $('#sel-file-btn').on('click', function () {
        input.click();
    });

    input.addEventListener('change', function (e) {
        const files = e.target.files;
        const done = function (url) {
            input.value = '';
            image.src = url;
            $alert.hide();
            $modal.modal('show');
        };
        let reader;
        let file;

        if (files && files.length > 0) {
            file = files[0];

            if (URL) {
                done(URL.createObjectURL(file));
            } else if (FileReader) {
                reader = new FileReader();
                reader.onload = function (e) {
                    done(reader.result);
                };
                reader.readAsDataURL(file);
            }
        }
    });

    $modal.on('shown.bs.modal', function () {
        cropper = new Cropper(image, {
            viewMode: 3,
            guides: false,
            highlight: true
        });
    }).on('hidden.bs.modal', function () {
        cropper.destroy();
        cropper = null;
    });

    document.getElementById('crop').addEventListener('click', function () {
        let initialAvatarURL;
        let canvas;

        $modal.modal('hide');

        if (cropper) {
            canvas = cropper.getCroppedCanvas({
                width: 160,
                height: 160,
            });
            // initialAvatarURL = avatar.src;
            // avatar.src = canvas.toDataURL();
            $alert.removeClass('alert-success alert-warning');
            canvas.toBlob(function (blob) {
                const formData = new FormData();
                formData.append('img', blob);
                console.log(blob);
                $.ajax({
                    url: ajax_url,
                    type: 'POST',
                    data: formData,
                    contentType: false,
                    processData: false,
                    success: function (data) {
                        if (data.msg == "Success") {
                            $('#processed-img').empty();
                            $('#processed-img').html(`
                            <img src="${result_img}?${Math.random()}" id="res_img">
                            `);
                            btnSave.show();
                            console.log('Success');
                        }
                    },
                    error: function (data) {
                        console.log('Error');
                        console.log(data);
                    }
                });
            });
        }
    });
});