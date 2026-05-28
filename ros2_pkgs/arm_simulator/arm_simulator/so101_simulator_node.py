import os
import time
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import pybullet as p
import pybullet_data

# ROS2のパッケージ位置を取得するためのライブラリ
from ament_index_python.packages import get_package_share_directory

class SOArmSimulator(Node):
    def __init__(self):
        super().__init__('so_arm_simulator')
        
        # ROS2 サブスクライバー
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_callback,
            10)
        
        # PyBullet初期化
        p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)
        p.loadURDF("plane.urdf") 
        
        p.resetDebugVisualizerCamera(
            cameraDistance=0.8,    # アームからの距離（メートル）。値を小さくすると近づく
            cameraYaw=45,          # カメラの左右の回転（度）。45度斜めから見る
            cameraPitch=-30,       # カメラの上下の傾き（度）。-30度で見下ろす
            cameraTargetPosition=[0.1, 0.0, 0.0] # カメラが捉える中心点 [X, Y, Z]
        )
        
        # ★★★ ここがポイント ★★★
        # ROS2システムから、このパッケージのインストール先の絶対パスを取得します
        package_share_dir = get_package_share_directory('arm_simulator')
        
        # パッケージ内のURDFへの絶対パスを組み立てる
        urdf_path = os.path.join(package_share_dir, 'urdf', 'so101_new_calib.urdf')
        
        # URDFがあるフォルダ（share/so101_simulator/urdf）にカレントディレクトリを一時的に変更する
        # これにより、URDF内の `filename="assets/..."` という相対パスが正しく解決されます
        original_cwd = os.getcwd()
        os.chdir(os.path.dirname(urdf_path))
        
        try:
            # アームを固定してロード
            self.robot_id = p.loadURDF(urdf_path, [0, 0, 0], useFixedBase=True)
            self.get_logger().info(f"成功: パッケージ内から URDF を読み込みました。")
        except Exception as e:
            self.get_logger().error(f"URDFの読み込みに失敗しました: {e}")
            return
        finally:
            # 念のため、元のカレントディレクトリに復原しておく
            os.chdir(original_cwd)

        # （以下、関節情報の取得やコールバック関数は前と同じ）
        self.movable_joints = []
        for i in range(p.getNumJoints(self.robot_id)):
            info = p.getJointInfo(self.robot_id, i)
            joint_type = info[2]
            if joint_type in [p.JOINT_REVOLUTE, p.JOINT_PRISMATIC]:
                self.movable_joints.append(i)

    def joint_callback(self, msg):
        for i, angle in enumerate(msg.position):
            if i < len(self.movable_joints):
                p.setJointMotorControl2(
                    bodyIndex=self.robot_id,
                    jointIndex=self.movable_joints[i],
                    controlMode=p.POSITION_CONTROL,
                    targetPosition=angle
                )

def main():
    rclpy.init()
    node = SOArmSimulator()
    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.001)
            p.stepSimulation()
            time.sleep(1./240.)
    except KeyboardInterrupt:
        pass
    finally:
        p.disconnect()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()