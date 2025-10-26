import { Canvas, useFrame } from "@react-three/fiber"
import { OrbitControls } from "@react-three/drei"
import { Physics, RigidBody, useRapier } from "@react-three/rapier"
import { Suspense, useRef, useEffect, useState } from "react"

// export default function SceneRenderer({ data }) {
//   if (!data || !data.scene) {
//     return (
//       <div className="text-white text-lg text-center">
//         <div className="text-center text-gray-300">
//             <h2 className="text-4xl font-bold text-white mb-3">
//                 3D Simulation View
//             </h2>
//             <p className="text-gray-400 text-lg max-w-sm mx-auto">
//                 Enter a problem and click <span className="text-[#31E3CB] font-semibold">Update Problem</span> to generate a simulation.
//             </p>
//         </div>
//       </div>
//     )
//   }
//   console.log(data)
//   const cameraPos = data.scene.camera?.position || { x: 80, y: 40, z: 80 }
//   const lighting = data.scene.lighting || []
//   const objects = data.scene.objects || []
//   const environment = data.scene.environment || null

//   return (
//     <Canvas
//         camera={{
//             position: [40, 25, 60], 
//             fov: 45,
//             near: 0.1,
//             far: 500,
//         }}
//         style={{ width: "100%", height: "100%" }}
//         >
//       <Suspense fallback={null}>
//         <OrbitControls
//           enablePan={false}
//           enableZoom={true}
//           enableRotate={true}
//           minDistance={50}
//           maxDistance={150}
//           target={[0, 0, 0]}
//         />
//         <SceneLights lighting={lighting} />
//         <Physics gravity={[0, -9.81, 0]}>
//           <RigidBody type="fixed">
//             <StrongBase />
//           </RigidBody>
//           <EnvironmentRigid environment={environment} />
//           <SceneObjectsRigid objects={objects} environment={environment} />
//         </Physics>
//       </Suspense>
//     </Canvas>
//   )
// }
export default function SceneRenderer({ data, replaySignal }) {
    if (!data || !data.scene) {
        return (
        <div className="text-white text-lg text-center">
            <div className="text-center text-gray-300">
                <h2 className="text-4xl font-bold text-white mb-3">
                    3D Simulation View
                </h2>
                <p className="text-gray-400 text-lg max-w-sm mx-auto">
                    Enter a problem and click <span className="text-[#31E3CB] font-semibold">Update Problem</span> to generate a simulation.
                </p>
            </div>
        </div>
        )
    }
  const [resetFlag, setResetFlag] = useState(false)
   console.log(data)
   const cameraPos = data.scene.camera?.position || { x: 80, y: 40, z: 80 }
  const lighting = data.scene.lighting || []
  const objects = data.scene.objects || []
  const environment = data.scene.environment || null
  useEffect(() => {
    if (replaySignal) setResetFlag(true)
  }, [replaySignal])

  return (
    <Canvas
      camera={{ position: [75, 40, -80], fov: 45 }}
      style={{ width: "100%", height: "100%" }}
    >
      <Suspense fallback={null}>
        <OrbitControls
          enablePan={false}
          enableZoom={true}
          enableRotate={true}
          minDistance={50}
          maxDistance={150}
          target={[0, 0, 0]}
        />
        <SceneLights lighting={lighting} />
        <Physics gravity={[0, -9.81, 0]}>
          <RigidBody type="fixed"><StrongBase /></RigidBody>
          <EnvironmentRigid environment={data.scene.environment} />
          <SceneObjectsRigid
            objects={objects}
            environment={environment}
            resetFlag={resetFlag}
            onResetDone={() => setResetFlag(false)}
          />
        </Physics>
      </Suspense>
    </Canvas>
  )
}

function StrongBase() {
  return (
    <mesh position={[0, -0.75, 0]} receiveShadow castShadow>
      <boxGeometry args={[60, 1.5, 60]} />
      <meshStandardMaterial color="#9CA3AF" roughness={0.6} metalness={0.3} />
    </mesh>
  )
}

function EnvironmentRigid({ environment }) {
  if (!environment) return null

  const type = environment.type || "plane"
  const angleDeg = environment.angle || 0
  const angle = angleDeg * (Math.PI / 180)
  const color = environment.material?.color || "#AAAAAA"

  if (type !== "incline") return null

  const widthX = 30
  const thicknessY = 0.8
  const lengthZ = 30
  const centerY = (thicknessY * 0.5) * Math.cos(angle) + (lengthZ * 0.5) * Math.sin(angle) + 0.0005

  return (
    <RigidBody type="fixed" position={[0, centerY, 0]}>
      <mesh rotation={[-angle, 0, 0]} receiveShadow castShadow>
        <boxGeometry args={[widthX, thicknessY, lengthZ]} />
        <meshStandardMaterial color={color} roughness={0.7} metalness={0.15} />
      </mesh>
    </RigidBody>
  )
}

function SceneObjectsRigid({ objects = [], environment, resetFlag, onResetDone }) {
  const bodiesRef = useRef([])

  useEffect(() => {
    if (resetFlag && bodiesRef.current.length) {
      bodiesRef.current.forEach((bodyData) => {
        if (bodyData) {
          const { body, initial } = bodyData
          body.setTranslation(initial, true)
          body.setLinvel({ x: 0, y: 0, z: 0 }, true)
          body.setAngvel({ x: 0, y: 0, z: 0 }, true)
        }
      })
      onResetDone()
    }
  }, [resetFlag, onResetDone])

  const angleDeg = environment?.angle || 0
  const angle = (angleDeg * Math.PI) / 180
  const inclineThickness = 0.8
  const inclineLength = 30

  return (
    <>
      {objects.map((obj, i) => {
        const { type: objType, size = {}, material = {} } = obj
        const color = material.color || "#E2562C"
        const radius = (size.radius || 1.5) * 3
        const topY =
          (inclineThickness * Math.cos(angle)) +
          (inclineLength * Math.sin(angle)) * 0.5 +
          radius * 0.8
        const topZ =
          -Math.sin(angle) * (inclineLength * 0.5)
        const pos = [0, topY, topZ]

        return (
          <RigidBody
            key={i}
            colliders={objType === "sphere" ? "ball" : "cuboid"}
            restitution={material.restitution ?? 0.3}
            friction={material.friction ?? 0.4}
            position={pos}
            ref={(ref) => {
              if (ref)
                bodiesRef.current[i] = { body: ref, initial: { x: pos[0], y: pos[1], z: pos[2] } }
            }}
          >
            <mesh castShadow receiveShadow>
              {objType === "sphere"
                ? <sphereGeometry args={[radius, 32, 32]} />
                : <boxGeometry args={[3, 3, 3]} />}
              <meshStandardMaterial color={color} roughness={0.5} metalness={0.2} />
            </mesh>
          </RigidBody>
        )
      })}
    </>
  )
}


function SceneLights({ lighting }) {
  return (
    <>
      <pointLight position={[0, 50, 50]} intensity={1.2} />
      <ambientLight intensity={0.4} color="#b0c4de" />
      <directionalLight position={[10, 15, 10]} intensity={1.2} castShadow color="#ffffff" />
      <directionalLight position={[-10, 5, -10]} intensity={0.6} color="#f5e0b7" />
      {lighting?.map((light, i) => {
        if (light.type === "ambient") {
          return <ambientLight key={i} intensity={light.intensity || 0.5} />
        }
        if (light.type === "directional") {
          const dir = light.direction || { x: 1, y: -1, z: 1 }
          return (
            <directionalLight
              key={i}
              intensity={light.intensity || 0.8}
              position={[dir.x * 10, dir.y * 10, dir.z * 10]}
            />
          )
        }
        return null
      })}
    </>
  )
}


// function SceneObjectsRigid({ objects = [], environment }) {
//   if (!objects.length) return null

//   const angleDeg = environment?.angle || 0
//   const angle = (angleDeg * Math.PI) / 180
//   const inclineThickness = 0.8
//   const inclineLength = 30

//   return (
//     <>
//       {objects.map((obj, i) => {
//         const { type: objType, size = {}, material = {} } = obj
//         const color = material.color || "#E2562C"
//         const radius = (size.radius || 1.5) * 3

//         const topOfInclineY =
//           (inclineThickness * Math.cos(angle)) +
//           (inclineLength * Math.sin(angle)) * 0.5 +
//           radius * 0.8
//         const topOfInclineZ =
//           -Math.sin(angle) * (inclineLength * 0.5)

//         const pos = [0, topOfInclineY, topOfInclineZ]

//         return (
//           <RigidBody
//             key={i}
//             colliders={objType === "sphere" ? "ball" : "cuboid"}
//             restitution={material.restitution ?? 0.3}
//             friction={material.friction ?? 0.4}
//             position={pos}
//           >
//             <mesh castShadow receiveShadow>
//               {objType === "sphere" ? (
//                 <sphereGeometry args={[radius, 32, 32]} />
//               ) : (
//                 <boxGeometry args={[3, 3, 3]} />
//               )}
//               <meshStandardMaterial
//                 color={color}
//                 roughness={0.5}
//                 metalness={0.2}
//                 emissive={color}
//                 emissiveIntensity={0.15}
//               />
//             </mesh>
//           </RigidBody>
//         )
//       })}
//     </>
//   )
// }