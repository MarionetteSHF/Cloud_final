var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);
var apigClient = apigClientFactory.newClient();

var token = null;

const signUp = () => {
  event.preventDefault();
  console.log("signup");
  const username = document.querySelector("#inputUsername").value;
  const emailadd = document.querySelector("#inputEmail").value;
  const password = document.querySelector("#inputPassword").value;
  const phone = document.querySelector("#phonenumber").value;
  console.log(phone);
  console.log(username);
  console.log(password);
  var email = new AmazonCognitoIdentity.CognitoUserAttribute({
    Name: "email",
    Value: emailadd,
  });

  userPool.signUp(username, password, [email], null, function (err, result) {
    if (err) {
      alert(err);
    } else {
      console.log(result);
      // this is not working, clockdrift changes overtime
      // const k = `CognitoIdentityServiceProvider.${poolData.ClientId}.${username}.clockDrift`;
      // const user_id = getCurrentUser().storage[k];
      // console.log(user_Id);

      // register in dynamoDB user database
      var params = {
        // user_id : user_id,
        username : username,
        email : emailadd,
        password : password,
        phone : phone
      };
      var body = {
        // user_id : user_id,
        username : username,
        email : emailadd,
        password : password,
        phone : phone
      };
      var additionalParams = {};
      apigClient.createuserPost(params,body,additionalParams)
          .then(function(result){
              console.log("New user is added to dynamoDB!");
              console.log(result.data);
          });

      // log in in local device
      signIn(username, password);
    }
  });


};



// const confirmCode = () => {
//   event.preventDefault();
//   const username = location.hash.substring(1);
//   const cognitoUser = new AmazonCognitoIdentity.CognitoUser({
//     Username: username,
//     Pool: userPool,
//   });
//   const code = document.querySelector("#confirm").value;
//   console.log("code =" + code);
//   cognitoUser.confirmRegistration(code, true, function (err, results) {
//     if (err) {
//       alert(err);
//     } else {
//       console.log("confirmed");
//       location.href = "signin.html";
//     }
//   });
// };

// const resendCode = () => {
//   event.preventDefault();
//   const username = location.hash.substring(1);
//   const cognitoUser = new AmazonCognitoIdentity.CognitoUser({
//     Username: username,
//     Pool: userPool,
//   });
//   cognitoUser.resendConfirmationCode(function (err) {
//     if (err) {
//       alert(err);
//     }
//   });
// };

const signIn = (username, password) => {
  if (username===undefined || password===undefined) {
    event.preventDefault();
    console.log("get login");
    username = document.querySelector("#inputUsername-1").value;
    password = document.querySelector("#inputPassword-1").value;    
  }

  console.log(userPool,username)
  let authenticationData = {
    Username: username,
    Password: password
  };

  var authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails(
    authenticationData
  );
  var userData = {
    Username: username,
    Pool: userPool
  };

  var cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);
  cognitoUser.authenticateUser(authenticationDetails, {
    onSuccess: function () {
      console.log("login success");
      location.href = "/index.html";
    },
    onFailure: function (err) {
      console.log("login FAILURE")
      alert(JSON.stringify(err));
    },
  });
};

const signOut = () => {
  console.log("sign out");
  var cognitoUser = userPool.getCurrentUser();
  if (cognitoUser) cognitoUser.signOut();
};


const getCurrentUser = () => {
  var cognitoUser = userPool.getCurrentUser();
  if (cognitoUser != null) {
    return cognitoUser;
  } else {
    console.log("NOT LOGIN YET")
    return cognitoUser;
  }
};



const checkLogin = () => {
  console.log("checking login..");
  const login = false;
  const userBtn = document.querySelector(".user");
  const leftBtn = document.querySelector(".left");
  const rightBtn = document.querySelector(".right");
  var cognitoUser = userPool.getCurrentUser();
  if (cognitoUser != null) {
    userBtn.innerHTML += cognitoUser.username;
    rightBtn.classList.toggle("hide");
  } else {
    leftBtn.innerHTML = "Sign In";
    rightBtn.innerHTML = "Register";
  }
};

const navTosignUp = () => {
  console.log("sign up");
  location.href = "signup.html";
};

const navTosignIn = () => {
  console.log("sign in");
  var cognitoUser = userPool.getCurrentUser();
  if (cognitoUser !== null) {
    location.href = "friends.html";
  } else {
    location.href = "signin.html";
  }
};

const loadUsers = () => {
  getJWTToken(function (token) {
    apigClient
      .usersGet({}, null, { headers: { Authorization: token } })
      .then(function (result) {
        console.log(result);
        displayUsers(result.data);
      })
      .catch((err) => console.log(err));
  });
};

function refresh(){
  const userBtn = document.querySelector(".user");
  var cognitoUser = userPool.getCurrentUser();
  if (cognitoUser != null) {
    userBtn.innerHTML += cognitoUser.username;
  }
}

function displayUsers(data) {
  const chatContainer = document.querySelector(".container");
  data.forEach((user) => {
    // <div class="conv">
    //     <p class="conv-text">Student - frank</p>
    //     <button class="conv-btn">details</button>
    // </div>
    const div = document.createElement("div");
    div.classList.add("conv");

    const p = document.createElement("p");
    p.classList.add("conv-text");
    p.innerText = user.Username;
    div.appendChild(p);

    const t = document.createElement("p");
    t.classList.add("time");
    t.innerText = "today";
    div.appendChild(t);

    const btn = document.createElement("button");
    btn.classList.add("conv-btn");
    //btn.innerHTML = '<i class="fas fa-comment"></i>';
    btn.innerText = "Start Chat";
    btn.addEventListener("click", () => startChat(user.Username));
    div.appendChild(btn);
    chatContainer.append(div);
  });
}

function startChat(userName) {
  console.log(userName);
  //postChats();
  location.href = "chat.html#" + userName;
}

function getJWTToken(callback) {
  if (token == null) {
    var cognitoUser = userPool.getCurrentUser();
    if (cognitoUser != null) {
      cognitoUser.getSession(function (err, session) {
        if (err) {
          location.href = "index.html";
        }
        token = session.getIdToken().getJwtToken();
        console.log("---------------");
        console.log(token);
        console.log("---------------");
        callback(token);
      });
    }
  } else {
    callback(token);
  }
}

function hashString(s) {
  return s.split("").reduce(function (a, b) {
    a = (a << 5) - a + b.charCodeAt(0);
    return a & a;
  }, 0);
}
function getUniqueName(curUser, otherUser) {
  curUser = curUser.toLowerCase();
  otherUser = otherUser.toLowerCase();

  let user_name = curUser + "_" + otherUser;
  if (curUser.length === otherUser.length) {
    if (hashString(curUser) < hashString(otherUser)) {
      return otherUser + "_" + curUser;
    }
  } else if (otherUser.length > curUser.length) {
    return otherUser + "_" + curUser;
  }
  return user_name;
}

function loadChatDetails(otherUser) {
  getJWTToken(function (token) {
    let cognitoUser = userPool.getCurrentUser();
    let curUser = cognitoUser.username;
    let unique_name = getUniqueName(curUser, otherUser);
    apigClient
      .chatsGet({ sender_receiver: unique_name }, null, { headers: { Authorization: token } })
      .then(function (result) {
        console.log(result);
        chats = result.data;
        displayChatDetails(chats, curUser, otherUser)
        
      })
      .catch((err) => console.log(err));
    });
}

function displayChatDetails(chats,curUser,otherUser) {
  const chatContainer = document.querySelector(".message-container");
  chatContainer.innerHTML = "";
  //console.log("chats= " + conv.messages);
  //const messages = conv.messages;
  const defaultUser = curUser;
  chats.forEach((chat) => {
    // <div class="message left">
    //      <p class="sender">sender</p>
    //      <p class="msg-text">This is a sample message</p>
    //      <p class="time">15 minutes ago</p>
    // </div>
    // div
    const direction = chat.sender === defaultUser ? "left" : "right";
    const div = document.createElement("div");
    div.classList.add("message");
    div.classList.add(direction);

    const pSender = document.createElement("p");
    pSender.classList.add("sender");
    pSender.innerText = chat.sender;
    div.appendChild(pSender);

    const pMessage = document.createElement("p");
    pMessage.classList.add("msg-text");
    pMessage.innerText = chat.message;
    div.appendChild(pMessage);

    const pTime = document.createElement("p");
    pTime.classList.add("time");
    console.log("time = " + chat.unixtime);
    const d = new Date(Number(chat.unixtime)*1000);
    console.log("date = " + d);
    pTime.innerText = moment(d).fromNow();
    div.appendChild(pTime);

    chatContainer.appendChild(div);
  });
}

function postChat() {
  let cognitoUser = userPool.getCurrentUser();
  let curUser = cognitoUser.username;
  otherUser = location.hash.substring(1);

  let unique_name = getUniqueName(curUser, otherUser);

    const msgInput = document.querySelector(".msg-input");
    var msg = msgInput.value;
    if (msg === "") return;
    msgInput.value = "";
    console.log("post chat !" + msg);

    const now = new Date()  
    const secondsSinceEpoch = Math.round(now.getTime() / 1000)  

  var payload = {
    sender_receiver: unique_name,
    unixtime: secondsSinceEpoch,
    sender: curUser,
    receiver: otherUser,
    message: msg
  };
  apigClient
    .chatsPost({ sender_receiver: unique_name }, payload, { headers: { Authorization: token } } )
    .then(function (result) {
      console.log('success post !');
      console.log(result);
    })
    .catch((err) => console.log(err));
}