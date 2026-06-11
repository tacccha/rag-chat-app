import ChatMessage from "./ChatMessage";

export default function ChatHistory({ histories, bottomRef, loading }) {
    return (
        <div
            className="
                flex-1
                overflow-y-auto
                p-6
                bg-gray-50
            "
        >
            {histories.length === 0 && !loading && (
                <div
                    className="
                            h-full
                            flex
                            items-center
                            justify-center
                            text-gray-400
                        "
                >
                    質問してください
                </div>
            )}

            <div
                className="
                    flex
                    flex-col
                    gap-6
                "
            >
                {histories.map((history, index) => (
                    <ChatMessage key={index} history={history} />
                ))}

                {/* Loading Message */}

                {loading && (
                    <div className="flex justify-start">
                        <div
                            className="
                                    bg-white
                                    border
                                    rounded-2xl
                                    px-4
                                    py-3
                                    shadow-sm
                                "
                        >
                            <div
                                className="
                                        text-sm
                                        font-bold
                                        mb-2
                                    "
                            >
                                AI
                            </div>

                            <div
                                className="
                                        flex
                                        items-center
                                        gap-2
                                        text-gray-500
                                    "
                            >
                                <div
                                    className="
                                            w-2
                                            h-2
                                            bg-gray-400
                                            rounded-full
                                            animate-bounce
                                        "
                                />

                                <div
                                    className="
                                            w-2
                                            h-2
                                            bg-gray-400
                                            rounded-full
                                            animate-bounce
                                            [animation-delay:0.2s]
                                        "
                                />

                                <div
                                    className="
                                            w-2
                                            h-2
                                            bg-gray-400
                                            rounded-full
                                            animate-bounce
                                            [animation-delay:0.4s]
                                        "
                                />

                                <span>AIが考えています...</span>
                            </div>
                        </div>
                    </div>
                )}

                <div ref={bottomRef} />
            </div>
        </div>
    );
}
