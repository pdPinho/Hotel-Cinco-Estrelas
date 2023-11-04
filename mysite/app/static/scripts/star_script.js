function check_stars(rating){
    var doc = document.getElementById("stars");
    var stars = doc.getElementsByTagName("i");
    for (let i = 0; i < 5; i++) { 
        stars[i].classList.remove("checked");
    }

    for (let i = 0; i < rating.title; i++) { 
        stars[i].classList.add("checked");
    }

    document.getElementById("id_rating").value = rating.title;
}