/*methods for validate actions on wall, comment on another post, etc*/

async function sendNewPost(e)
{
  /*post new message on wall user.
  This send a request to back end to save and update tthe front
  */
  e.preventDefault();
  let myBody = new FormData();
  myBody.append("message", e.target.user_activity.value);
  let response = await fetch("post_on_wall", {
    method: "POST",
    body : myBody
  });
  if(!response.ok) {
    console.log("error resp", response);
    return false;
  }
  let html = await response.text();
  let newMsg = document.createElement("li");
  newMsg.innerHTML += html;
  /* send message to wall*/
  let firstMsgOnWall = document.querySelector(".panel-activity__list").firstElementChild;
  //console.log(firstMsgOnWall , newMsg);
  document.querySelector(".panel-activity__list").insertBefore(newMsg, firstMsgOnWall);

  e.target.user_activity.value = "";
  return true;
}


document.querySelector("#post-box").onsubmit = sendNewPost;
