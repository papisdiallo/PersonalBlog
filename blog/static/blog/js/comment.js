const commentForm = document.getElementById('commentForm');
const commentUl = document.getElementById('commentUl');
console.log(commentUl);
console.log(commentForm);
const content = document.getElementById('id_content');
url = window.location.href + "comments/"
csrftoken = document.getElementsByName('csrfmiddlewaretoken');
console.log(csrftoken);


commentForm.addEventListener('submit', e => {
    e.preventDefault()

    $.ajax({
        type: "POST",
        url: url,
        data: {
            'csrfmiddlewaretoken': csrftoken[0].value,
            'content': content.value
        },
        success: function (response) {
            console.log(response)
        },
        error: function (error) {
            console.log("Something went wrong with the comment", error);
        }
    });
});
