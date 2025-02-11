let userStatus=pstatus;
console.log(userStatus);

if(userStatus=="teacher"){
    let link1=document.getElementById("completedBtn");
    link1.hidden=false;
}
else if(userStatus=="admin"){
    let link1=document.getElementById("addTaskBtn");
    link1.hidden=false;
}