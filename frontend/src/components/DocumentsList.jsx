export default function DocumentsList({
    documents,

    handleDelete,
}) {
    return (
        <div
            className="
                mt-4
            "
        >
            <h3
                className="
                    text-lg
                    font-bold
                    mb-3
                "
            >
                Documents
            </h3>

            <div
                className="
                    border
                    rounded-xl
                    p-3
                    bg-gray-50
                "
            >
                {documents.length === 0 && (
                    <div
                        className="
                                text-gray-500
                                text-sm
                            "
                    >
                        No Documents
                    </div>
                )}

                {documents.map((document, index) => (
                    <div
                        key={index}
                        className="
                                    flex
                                    justify-between
                                    items-center
                                    py-2
                                    border-b
                                    last:border-b-0
                                "
                    >
                        <div
                            className="
                                        text-sm
                                        break-all
                                    "
                        >
                            {document}
                        </div>

                        <button
                            className="
                                        bg-red-300
                                        text-white
                                        px-3
                                        py-1
                                        rounded-lg
                                        text-sm
                                        hover:bg-red-600
                                        transition
                                        cursor-pointer
                                    "
                            onClick={() => handleDelete(document)}
                        >
                            Delete
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}
