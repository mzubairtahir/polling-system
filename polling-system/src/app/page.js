import CreatePollBtn from "@/components/CreatePollBtn";
import EditSvg from "@/components/EditSvg";
import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={`flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-600 text-white ${styles.container}`}>
      <div className="text-center">
        <h1 className="text-5xl font-extrabold mb-4">
          Create and Share Polls!
        </h1>
        <p className="text-lg mb-8">
        Create polls between two people and see who has the larger network. Share easily and gather insights quickly!


        </p>
        <div className="flex justify-center">

        <CreatePollBtn />
        </div>
      </div>
    </div>
  );
}
