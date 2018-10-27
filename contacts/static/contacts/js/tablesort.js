/**
 * The script which take cares of the elements responsible for sorting.
 *
 * Use #order-manager element to pass context data
 *      eg. <div type="hidden" id="order-manager" data-orderby="{{ orderby }}" data-order="{{ order }}"></div>
 *
 * The elements reponsible for sorting should have dataset with 'orderby' and 'order' values
 *      eg. <a data-orderby="city" data-order="asc" href="?page={{ page_obj.number }}" class="fas fa-sort-alpha-down ml-2 order"></a>
 *
 * WARNING!
 * The script append by '&' character get parameters 'order and 'orderby' to href value
 * if there is no '?' in href link will be incorrect
 *
 */

$( document ).ready(function() {

    let orderManager = $('#order-manager');
    let orderby = orderManager.data('orderby');
    let order = orderManager.data('order');

    if ((orderby !== undefined) && (order !== undefined)) {
        let sortElements = $('.order');
        sortElements.each(function() {
            let sortElementOrderBy = $(this).data('orderby');
            let sortElementOrder = $(this).data('order');
            let href = $(this).attr('href');
            let newHref = href + '$orderby=' + sortElementOrderBy + '&order=' + sortElementOrder;
            $(this).attr('href', newHref);
            if ((sortElementOrderBy == orderby) && (sortElementOrder == order)) {
                $(this).addClass('order-active')
            }
        })
    }

});
