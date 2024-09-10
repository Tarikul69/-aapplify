document.getElementById("toggleButton").addEventListener("click", function() {
    const openIcon = document.getElementById("openIcon");
    const closeIcon = document.getElementById("closeIcon");
    const mobileMenu = document.getElementById("mobileMenu");

    if (openIcon.classList.contains("hidden")) {

        openIcon.classList.remove("hidden");
        closeIcon.classList.add("hidden");
        mobileMenu.classList.add("translate-x-96")
        mobileMenu.classList.remove("translate-x-0")

    } else {
        openIcon.classList.add("hidden");
        closeIcon.classList.remove("hidden");
        mobileMenu.classList.add("translate-x-0")
        mobileMenu.classList.remove("translate-x-96")
    }
  });

  function closeMobileMenu() {
    const mobileMenu = document.getElementById("mobileMenu");
    const openIcon = document.getElementById("openIcon");
    const closeIcon = document.getElementById("closeIcon");

    mobileMenu.classList.add("translate-x-96");
    mobileMenu.classList.remove("translate-x-0");
    openIcon.classList.remove("hidden");
    closeIcon.classList.add("hidden");
}

document.getElementById("closeSide").addEventListener("click", closeMobileMenu);
document.querySelectorAll(".mobile_menu_list").forEach(function(element) {
    element.addEventListener("click", closeMobileMenu);
});


