import { useState, useEffect } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

function App() {
  const [isRecording, setisRecording] = useState(false);
  const [note, setNote] = useState<string>(null);
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;
  const microphone = new SpeechRecognition();

  microphone.continuous = true;
  microphone.interimResults = true;
  microphone.lang = "en-US";

  const saveUser = (uuid: string) => {
    //save to localstorage
    window.localStorage.setItem("pets-care-uuid", uuid);
  };

  const getUser = () => {
    window.localStorage.getItem("pets-care-uuid");
  };

  const startRecordController = () => {
    if (isRecording) {
      microphone.start();
      microphone.onend = () => {
        console.log("continue..");
        microphone.start();
      };
    } else {
      microphone.stop();
      microphone.onend = () => {
        console.log("Stopped microphone on Click");
      };
    }
    microphone.onstart = () => {
      console.log("microphones on");
    };

    microphone.onresult = (event: any) => {
      const recordingResult = Array.from(event.results)
        .map((result: any[]) => result[0])
        .map((result) => result.transcript)
        .join("");
      setNote(recordingResult);
      microphone.onerror = (event: unknown) => {
        console.log(event.error);
      };
    };
  };

  useEffect(() => {
    startRecordController();
  }, [isRecording]);

  return (
    <>
      <h3>
        {/* <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p> */}
        {note}
      </h3>
      <button onClick={() => setisRecording((prevState) => !prevState)}>
        {isRecording ? "Stop" : "Start"}
      </button>
    </>
  );
}

export default App;
