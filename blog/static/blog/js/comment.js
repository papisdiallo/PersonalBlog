const commentForm = document.getElementById('commentForm');
const commentUl = document.getElementById('commentUl');
const content = document.getElementById('id_content');
const commentsUlLi = document.getElementById('comment-list')
url = window.location.href + "comments/"
csrftoken = document.getElementsByName('csrfmiddlewaretoken');
const commentCount = document.getElementById('count');

commentForm.addEventListener('submit', e => {
    e.preventDefault()

    $.ajax({
        type: "POST",
        url: url,
        data: {
            'csrfmiddlewaretoken': csrftoken[0].value,
            'content': content.value
        },
        success: function (data) {
            $('#comment-list').append(data)
            content.value = "";
            let count = commentCount.textContent
            commentCount.textContent = parseInt(count) + 1
        },

        error: function (error) {
            console.log("Something went wrong with the comment", error);
        }
    });
});
