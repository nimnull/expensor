/**
 * Created with PyCharm.
 * User: nimnull
 * Date: 8/5/13
 * Time: 3:53 PM
 * To change this template use File | Settings | File Templates.
 */
(function($){
    $(function() {
       $("[data-action=add-commission]").on('click', function(event) {
           var formAction = $(event.currentTarget).attr('data-target');
           $(event.currentTarget.hash).find('form').attr({action: formAction});
           $(event.currentTarget.hash).modal();
           return false;
       });
    });
})(jQuery);

