(ros::roseus-add-msgs "soft_exterior_hand")
(load "package://aeroeus/aero-interface.l")
(aero-init)
(send *aero* :angle-vector (send *ri* :state :potentio-vector))

(ros::advertise "/servo_states" soft_exterior_hand::UInt16Array 1)

(setq pub-msg (instance soft_exterior_hand::UInt16Array :init))
(send pub-msg :data #i(80 107 128 120 160 30 180 270))
(ros::publish "/servo_states" pub-msg)
(ros::duration-sleep 0.8)

;;手の平が上向き
(send *aero* :angle-vector #f(-13.97 -9.97 -17.01 -135.1 0.0 0.0 0.0 -0.05 -4.98 9.97 19.98 -80.02 89.0 4.98 -19.9 0.0 0.0 24.9 -0.013 0.0 0.0 0.0 42.4 -60.9 -42.4 60.9))
(send *aero* :neck_p_joint :joint-angle 40)
(send *aero* :neck_y_joint :joint-angle 30)
(send *ri* :angle-vector (send *aero* :angle-vector) 3000)
(send *ri* :wait-interpolation)
(send *ri* :speak-jp "お手をどうぞ")

(setq cnt 0)
(while (< cnt 2)
  (setq cnt 0)
  (let ((sensor-states (one-shot-subscribe "/sensor_states" soft_exterior_hand::UInt16Array :timeout 20000)))
    (setq data (send sensor-states :data))
    (dotimes (i 14)
      (when (> (elt data i) 10)
        (setq cnt (+ cnt 1))))
))

;;指の間を開く
(setq pub-msg (instance soft_exterior_hand::UInt16Array :init))
(send pub-msg :data (integer-vector 120 128 125 102 180 30 180 270))
(ros::publish "/servo_states" pub-msg)
(ros::duration-sleep 1.5)

;;センサを見ながら指を曲げる
(setq cnt 0)
(setq deg 270)
(while (< cnt 2)
  (setq cnt 0)
  (let ((sensor-states (one-shot-subscribe "/sensor_states" soft_exterior_hand::UInt16Array :timeout 20000)))
    (setq data (send sensor-states :data))
    (dotimes (i 14)
      (when (> (elt data i) 10)
        (setq cnt (+ cnt 1))))
    (setq deg (- deg 30))
    (when (< deg 20)
      (exit))
    (send pub-msg :data (integer-vector 120 128 125 102 180 30 180 deg))
    (ros::publish "/servo_states" pub-msg)
    (ros::duration-sleep 0.2)
))

(send pub-msg :data (integer-vector 120 128 125 102 150 30 40 deg))
(ros::publish "/servo_states" pub-msg)

(send *aero* :neck_p_joint :joint-angle 25)
(send *aero* :neck_y_joint :joint-angle 0)
(send *ri* :angle-vector (send *aero* :angle-vector) 500)
(send *ri* :wait-interpolation)

(send *ri* :speak-jp "行きましょう" :wait t)
(send *ri* :go-velocity 0.1 0 0 5000 :wait t)

(setq pub-msg (instance soft_exterior_hand::UInt16Array :init))
(send pub-msg :data (integer-vector 120 128 125 102 160 30 180 200))
(ros::publish "/servo_states" pub-msg)
(ros::duration-sleep 0.5)

(setq pub-msg (instance soft_exterior_hand::UInt16Array :init))
(send pub-msg :data (integer-vector 120 128 125 102 180 30 180 270))
(ros::publish "/servo_states" pub-msg)


