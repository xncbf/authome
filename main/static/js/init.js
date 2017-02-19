(function ($) {
    $(function () {

        //모달 트리거
        $('.modal').modal();
        $('.tooltipped').tooltip({
            delay: 50,
            html: true
        });
        $('.datepicker').pickadate({
            selectMonths: true, // Creates a dropdown to control month
            selectYears: 15, // Creates a dropdown of 15 years to control year
            format: 'yyyy-mm-dd'
        });
        $(document).ready(function () {
            $('select').material_select();
        });
    }); // end of document ready
})(jQuery); // end of jQuery name space