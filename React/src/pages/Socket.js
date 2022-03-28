import React, {useState, useEffect} from 'react'
import io from "socket.io-client";
import $ from 'jquery';

export default function Socket() {      
    var socket = io.connect(`${'http://localhost:5000/'}`);
    socket.on('connect', function() {
      socket.emit('user connect', {
        data: 'User Connected'
      } )
      var form = $('form').on('submit', function( e ) {
        e.preventDefault()
        let user_name = `{{ username }}`
        let user_input = $('input.msger-input').val()
        socket.emit('user response', {
          user_name : user_name,
          message : user_input
        } )
        $('input.msger-input').val( '' ).focus()
        $('input.username').hide()
      } )
    } )
    socket.on('user response', function( msg ) {
      var timestamp = Date().slice(16,21);
      if( typeof msg.user_name !== 'undefined' ) {
        $('main.msger-chat').append(`<div class="msg right-msg">
        <div
         class="msg-img"
         style="background-image: url({{ url_for('static',filename='assets/img/user.png')}})"
        ></div>
  
        <div class="msg-bubble">
          <div class="msg-info">
            <div class="msg-info-name">${msg.user_name}</div>
            <div class="msg-info-time">${timestamp}</div>
          </div>
  
          <div class="msg-text" style="overflow-wrap: anywhere;">
            ${msg.message}
          </div>
        </div>
      </div>
      `)
      }
    })
    socket.on('bot response', function( msg ) {
      var timestamp = Date().slice(16,21);
      if( typeof msg.user_name !== 'undefined' ) {
        $('main.msger-chat').append(`<div class="msg left-msg">
        <div
         class="msg-img"
         style="background-image: url(https://i.imgur.com/dbSQ4ZF.png)"
        ></div>
  
        <div class="msg-bubble">
          <div class="msg-info">
            <div class="msg-info-name">Manav</div>
            <div class="msg-info-time">${timestamp}</div>
          </div>
  
          <div class="msg-text">
            ${msg.response}
          </div>
        </div>
      </div>
      `)
      }
    })
    socket.on('bot greet', function( msg ) {
      var timestamp = Date().slice(16,21);
      if( typeof msg.user_name !== 'undefined' ) {
        $('main.msger-chat').append(`<div class="msg left-msg">
        <div
         class="msg-img"
         style="background-image: url(https://i.imgur.com/dbSQ4ZF.png)"
        ></div>
  
        <div class="msg-bubble">
          <div class="msg-info">
            <div class="msg-info-name">Manav</div>
            <div class="msg-info-time">${timestamp}</div>
          </div>
  
          <div class="msg-text">
            ${msg.greet}
          </div>
        </div>
      </div>
      `)
      }
    })
}
