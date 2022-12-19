function startFaceSession() {
    let pc = new RTCPeerConnection({
    iceServers: [
      {
        urls: 'stun:stun.l.google.com:19302'
      }
    ]
  })
  let log = msg => {
    document.getElementById('logdiv').innerHTML += msg + '<br>'
  }
  
  pc.ontrack = function (event) {
    var el = document.createElement(event.track.kind)
    el.srcObject = event.streams[0]
    el.autoplay = true
    el.controls = true
  
    document.getElementById('remoteVideos').appendChild(el)
  }
  
  pc.oniceconnectionstatechange = e => log(pc.iceConnectionState)
  pc.onicecandidate = event => {
    if (event.candidate === null) {
      document.getElementById('localSessionDescription').value = btoa(JSON.stringify(pc.localDescription))
    }
  }
  
  // Offer to receive 1 audio, and 2 video tracks
  pc.addTransceiver('audio', {'direction': 'recvonly'})
  pc.addTransceiver('video', {'direction': 'recvonly'})
  pc.addTransceiver('video', {'direction': 'recvonly'})
  pc.createOffer().then(d => pc.setLocalDescription(d)).catch(log)
  
  window.startRTCSession = () => {
    let sd = document.getElementById('remoteSessionDescription').value
    if (sd === '') {
      return alert('Session Description must not be empty')
    }
  
    try {
      pc.setRemoteDescription(new RTCSessionDescription(JSON.parse(atob(sd))))
    } catch (e) {
      alert(e)
    }
  }
}