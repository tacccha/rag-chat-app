export default function UploadSection({
    file,
    setFile,
    handleUpload,
    loading,
}) {
    return (
        <details
            className="
            border
            rounded-xl
            p-4
            bg-gray-50
        "
        >
            <summary
                className="
                cursor-pointer
                font-bold
            "
            >
                PDF Upload
            </summary>

            <div className="mt-4">
                <input
                    type="file"
                    onChange={(e) => setFile(e.target.files[0])}
                    className="
                    mb-3
                    block w-full text-sm
                "
                />

                <button
                    className="
                    bg-blue-500
                    text-white
                    px-4
                    py-2
                    rounded-xl
                    hover:bg-blue-600
                    disabled:bg-gray-400
                "
                    onClick={handleUpload}
                    disabled={loading || !file}
                >
                    アップロード
                </button>
            </div>
        </details>
    );
}
