const showWishlist = () =>{
    document.getElementById("wishlist").style.display = "block";
    document.getElementById("displayReview2").style.display = "none";
}

const showReviews = () =>{
    document.getElementById("wishlist").style.display = "none";
    document.getElementById("displayReview2").style.display = "block";
}

window.onload = function() {
    showWishlist();
};