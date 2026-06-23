import ReactMarkdown from "react-markdown";

export default function ChatMessage({ history }) {
    return (
        <div className="space-y-3">
            {/* Question */}

            <div className="flex justify-end">
                <div
                    className="
                        bg-blue-500
                        text-white
                        px-4
                        py-3
                        rounded-2xl
                        max-w-[75%]
                        shadow
                    "
                >
                    <div className="text-xs opacity-80 mb-1">You</div>

                    <div className="whitespace-pre-wrap">
                        {history.question}
                    </div>
                </div>
            </div>

            {/* Answer */}

            <div className="flex justify-start">
                <div
                    className="
                        bg-white
                        border
                        px-4
                        py-3
                        rounded-2xl
                        max-w-[75%]
                        shadow-sm
                    "
                >
                    <div
                        className="
                            text-xs
                            text-gray-500
                            mb-2
                        "
                    >
                        AI Assistant
                    </div>

                    <div
                        className="
                            prose
                            prose-sm
                            max-w-none
                        "
                    >
                        <ReactMarkdown>{history.answer}</ReactMarkdown>
                    </div>

                    {/* Sources */}

                    {history.sources?.length > 0 && (
                        <div className="mt-4">
                            <div
                                className="
                                        text-sm
                                        font-semibold
                                        mb-2
                                        text-gray-700
                                    "
                            >
                                Sources
                            </div>

                            <div className="space-y-2">
                                {history.sources.map((source, index) => (
                                    <div
                                        key={index}
                                        className="
                                                        border
                                                        rounded-lg
                                                        p-3
                                                        bg-gray-50
                                                        text-sm
                                                    "
                                    >
                                        <div
                                            className="
                                                            font-medium
                                                            text-gray-800
                                                        "
                                        >
                                            {source.title}
                                        </div>

                                        <div
                                            className="
                                                            text-gray-500
                                                            mt-1
                                                        "
                                        >
                                            Page: {source.page}
                                        </div>

                                        {/* <div
                                            className="
                                                            text-gray-400
                                                            text-xs
                                                            mt-1
                                                        "
                                        >
                                            Score: {source.score?.toFixed(3)}
                                        </div> */}
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
