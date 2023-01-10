Network/Cloud architecture
==========================

The network architecture of the software is built to enable, in the
future, multiple concurrent users interacting in a many-to-many fashion
with synthetic agents. Web browser is used as primary endpoint software,
avoiding distribution issues, with minimal/no edge processing.

Session Leader (SL)
-------------------

The session leader is the primary RPC endpoint for the website, speaking
JSON with the code we write.

This will contain session management and so forth, handling user
authentication and ensuring things like token budget.

The session leader should NEVER be performing computation, and instead
merely coordinating (as necessary) the other servers.

Face scheduler (FS)
-------------------

The face scheduler is reponsible for keeping track of which A2F face is
currently being used for which user.

Audio server (AS)
-----------------

The audio server receives data from browser and shuttles over to A2F.

Runs the WebRTC receiver.

Video proxy (VP)
----------------

The video proxy receives data from A2F and shuttles over to browser.

Runs the RTP receiver that ffmpeg sends to.

Example user session
---------------------

::

   User: opens link to speak to their avatar (contains SID)
   tutor.js: tell the SL we are here now (SID=...)
   SL -> FS: is there an available face?
   SL <- FS: {Yes it is $FID, No try again later}

   unique session id: CKEY=SecureCombination(SID,FID)

   SL -> AS: prepare for CKEY
   SL -> VP: prepare for CKEY
   SL -> tutor.js: You are user CKEY=SecureCombination(SID,FID)

   tutor.js -> AS: start WebRTC stream with CKEY
   tutor.js -> VP: start receiving stream with CKEY

Done! Now the session is established and the streams will be processed
on-demand.