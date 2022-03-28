import React from 'react';
import Socket from './Socket';
import {Link} from 'react-router-dom';

export default function Home() {
  return (
    <React.Fragment>  
        <div id='stars'></div>
    <div id='stars2'></div>
    <div id='stars3'></div>
  
  <section class="msger">
    <header class="msger-header">
      <div class="msger-header-title" style="font-weight: bolder;">
        <i class="fa fa-user-md"></i> 
        Manavta
         {/* <div class="version">{{ version }}</div> */}
      </div>
      <div class="msger-header-options">
      </div>
    </header>
  
    <main class="msger-chat" id="toscroll">
      <div class="msg right-msg">
      </div>
    </main>
  
    <form class="msger-inputarea">
      <a href=""><i class="fa fa-microphone" id="msger-mic"></i></a>
      <input type="text" class="msger-input" placeholder="Enter your message..."/>
      <input type="submit" class="msger-send-btn" value="Send"/>
    </form>
  </section>

    <Socket/> 
  
  {/* <script>
   const theElement = document.getElementById('toscroll');
  
  const scrollToBottom = (node) => {
      node.scrollTop = node.scrollHeight;
  }
  
  scrollToBottom(theElement);
  </script>
   */}
  
  </React.Fragment>
  )
}
