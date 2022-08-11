const toggleTab = (id) => {
    if (id === 'postcards'){
        document.getElementById('postcards-tab').style.display='flex';
        document.getElementById('posts-tab').style.display='none';
    } else if (id === 'posts') {
        document.getElementById('posts-tab').style.display='flex';
        document.getElementById('postcards-tab').style.display='none';
    }
}