(load "package://aeroeus/aero-interface.l")
(aero-init)
(send *aero* :angle-vector (send *ri* :state :potentio-vector))

(unix::sleep 5)
;; かがんで手を差し出す
(send *aero* :knee_joint :joint-angle -60)
(send *aero* :ankle_joint :joint-angle 70.0)
(send *aero* :waist_p_joint :joint-angle 32)

(send *aero* :l_shoulder_p_joint :joint-angle -50)
(send *aero* :l_elbow_joint :joint-angle -50)
(send *aero* :l_shoulder_r_joint :joint-angle 0)
(send *aero* :l_shoulder_y_joint :joint-angle 0)

(send *aero* :r_shoulder_p_joint :joint-angle -50)
(send *aero* :r_elbow_joint :joint-angle -50)
(send *aero* :r_shoulder_r_joint :joint-angle 0)
(send *aero* :r_shoulder_y_joint :joint-angle 0)

(send *aero* :r_wrist_r_joint :joint-angle 85)
(send *aero* :r_hand_y_joint :joint-angle -85)
(send *aero* :l_wrist_r_joint :joint-angle -85)
(send *aero* :l_hand_y_joint :joint-angle 85)

(send *ri* :angle-vector (send *aero* :angle-vector) 7000)
(send *ri* :wait-interpolation)

;; 人が手を掴んだことを検知
(unix::sleep 5)

;; 手を前に引く
(setq r-target-coords (send (send *aero* :rarm :end-coords :copy-worldcoords) :translate #f(-250 0 50) :world))
(setq l-target-coords (send (send *aero* :larm :end-coords :copy-worldcoords) :translate #f(-250 0 50) :world))
(send *aero* :waist_p_joint :joint-angle 10)
(send *aero* :rarm :inverse-kinematics r-target-coords)
(send *aero* :larm :inverse-kinematics l-target-coords)

(send *ri* :angle-vector (send *aero* :angle-vector) 3000)
(send *ri* :wait-interpolation)
;; 手を開く
