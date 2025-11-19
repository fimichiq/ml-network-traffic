import ModelList from "~/components/Models";
import FileList from "~/components/Files";

// max-w-7xl

function Classify() {
    return (
        <div className="grid grid-cols-2 gap-2 w-full">
            <ModelList />
            <FileList onRefresh={false} />
        </div>
    );
}

export default Classify;
