import React, { useState } from 'react';
import './App.css';
import Auth from './Auth';
import Chats from './Chats';

const App = () => {
  const [user,setUser] = useState(undefined);
  if(!user){
    return <Auth onAuth={user=> setUser(user)} />
  }
  else{
    return <Chats user={user} />
  }
}

export default App;