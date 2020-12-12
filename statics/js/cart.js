var updateBtns = document.getElementsByClassName("update-cart")
for(var i=0;i<3;i++)
{
    updateBtns[i].addEventListener('click', function(){
        var productId= this.dataset.product
        var action= this.dataset.action
        console.log(productId,action)

        console.log('USER',user)
        if (user=='AnonymousUser'){
            console.log('User is not authenticated')
        }
        else{
            UpdateUserOrder(productId,action)
        }
        }
    )
}

function UpdateUserOrder(productId, action){
    console.log("User logged In, updating cart...")

    var url='/updatecart/'

    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({
            'productId':productId,'action':action})
    })

    .then((response) =>{
        return response.json()
    })
    
    .then((data) =>{
        console.log('data',data)
        location.reload()
    })
}