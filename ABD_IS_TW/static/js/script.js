var menu_btn = document.querySelector("#menu-btn");
var sidebar = document.querySelector("#sidebar");
var container = document.querySelector(".my-container");
menu_btn.addEventListener("click", () => {
    sidebar.classList.toggle("active-nav");
    container.classList.toggle("active-cont");
});
const carousel = new Glide('.glide', {
    type: 'carousel',
    autoplay: 4000,
    gap: 10,
    peek: 300,
    perView: 1
});

carousel.mount();