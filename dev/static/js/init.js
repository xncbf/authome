(function ($) {
    $(function () {

        $('.button-collapse').sideNav();
        //모달 트리거
        $('.modal-trigger').leanModal();
        $('.tooltipped').tooltip({
            delay: 50,
            html: true
        });

    }); // end of document ready
})(jQuery); // end of jQuery name space