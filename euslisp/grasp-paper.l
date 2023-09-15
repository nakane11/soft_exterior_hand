(ros::roseus-add-msgs "soft_exterior_hand")
(load "package://aeroeus/aero-interface.l")
(aero-init)
(send *aero* :angle-vector (send *ri* :state :potentio-vector))

(ros::advertise "/servo_states" soft_exterior_hand::UInt16Array 1)

(send *ri* :angle-vector (send *aero* :reset-pose) 2000)
(send *ri* :wait-interpolation)

;; (send *aero* :angle-vector #f(-13.9589 -9.94925 -16.98 -135.148 0.0 0.0 0.0 -0.04 -17.5297 12.0707 -2.99088 -72.9976 -75.0 0.0 -8.73854 -37.3074 0.0 24.8837 0.012987 -2.16733 7.15406 0.0 40.9605 -38.9364 -40.9605 38.9364))
(send *aero* :angle-vector #f(-13.9589 -9.94925 -16.98 -135.148 0.0 0.0 0.0 -0.04 -19.481 9.79985 -0.673951 -72.0609 -70.5036 0.0 -14.7231 -45.3618 0.0 24.8837 0.012987 -1.83737 2.7461 0.0 38.0988 -34.262 -38.0988 34.262))
(send *ri* :angle-vector (send *aero* :angle-vector) 4000)
(send *ri* :wait-interpolation)
(ros::duration-sleep 0.5)

(send *aero* :inverse-kinematics
      (send (send *aero* :larm :end-coords :copy-worldcoords)
            :translate (float-vector 0 0 -200) :world)
      :ik-group :larm-whole-body
      :rotation-axis t
      :revert-if-fail t)
(send *ri* :angle-vector (send *aero* :angle-vector) 4000)
(send *ri* :wait-interpolation)

(setq pub-msg (instance soft_exterior_hand::UInt16Array :init))
(send pub-msg :data #i(80 107 128 120 60 30 180 30))
(ros::publish "/servo_states" pub-msg)
(ros::duration-sleep 1.0)

(send *aero* :inverse-kinematics                                             (send (send *aero* :larm :end-coords :copy-worldcoords)                      :translate (float-vector 0 0 150) :world)
        :ik-group :larm-whole-body                                                        :rotation-axis t                                                       :revert-if-fail t)
(send *ri* :angle-vector (send *aero* :angle-vector) 600)
(send *ri* :wait-interpolation)

(send *aero* :waist_y_joint :joint-angle 60)
(send *ri* :angle-vector (send *aero* :angle-vector) 1500)
(send *ri* :wait-interpolation)

(send *aero* :l_elbow_joint :joint-angle -85)
(send *ri* :angle-vector (send *aero* :angle-vector) 1000)
(send *ri* :wait-interpolation)
(send *ri* :speak-jp "書類をどうぞ":wait t)
(ros::duration-sleep 0.6)

(setq pub-msg (instance soft_exterior_hand::UInt16Array :init))
(send pub-msg :data #i(80 107 128 120 60 30 180 270))
(ros::publish "/servo_states" pub-msg)
(ros::duration-sleep 0.6)

(send *aero* :l_elbow_joint :joint-angle -50)
(send *ri* :angle-vector (send *aero* :angle-vector) 1000)
