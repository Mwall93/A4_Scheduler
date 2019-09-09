toastr.options = {
    "closeButton": false,
    "debug": false,
    "newestOnTop": true,
    "progressBar": true,
    "positionClass": "toast-top-right",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "6000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
}

function ShowDimmer() {
    $('#dimmer').addClass('active');
}

function HideDimmer() {
    $('#dimmer').removeClass('active');
}

function SubmitForm(name) {
    ShowDimmer();

    var form = $(`[data-form="${name}"]`);
    var url = form.attr('data-form-url');
    var onSubmitCb;
    var onCallbackCb;

    if(typeof onSubmitCb === 'function') {
        var result = onSubmitCb(ev);

        if(result === false) {
            HideDimmer();
            return;
        }
    }

    var cb = onCallbackCb;

    // make api request
    $.ajax({
        url: url,
        type: 'POST',
        data: form.first().serialize(),
        contentType: 'application/x-www-form-urlencoded',
        success: function(result) {
            HideDimmer();
            
            if(result.responseJSON !== undefined && result.responseJSON.data !== undefined && result.responseJSON.data.nice_message !== undefined) {
                toastr["success"](result.responseJSON.data.nice_message, "Success");
            }
            //console.log(result);

            if(typeof cb === 'function') {
                onCallbackCb(result);
            } else {
                location.reload();
            }

        },
        error: function(result) {
            HideDimmer();

            if(result.responseJSON !== undefined && result.responseJSON.data !== undefined && result.responseJSON.data.nice_message !== undefined) {
                toastr["error"](result.responseJSON.data.nice_message, "Error");
            }
            //console.log(result);
        }
    });
}

function OpenModal(modalName) {
    $(`[data-modal="${modalName}"]`).modal('show');
}

function CloseModal(modalName) {
    $(`[data-modal="${modalName}"]`).modal('hide');
}

/*((window, document) => {
    if(typeof window.config !== 'object')
        return;

    resource = new Resource(window.config.url);

    window.resource = resource;
})();*/

function DeleteRequest(url, redirect_to) {
    var result = confirm("Are you sure you want to delete this resource?");

    if(result !== true) {
        return;
    }

    $.ajax({
        url: url,
        type: 'DELETE',
        success: function(result) {
            window.location = redirect_to;
        }
    });
}

(() => {
    $('.ui.dropdown').dropdown();
})();