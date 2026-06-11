export default function QuestionInput({
    question,
    setQuestion,
    handleAsk,
    loading,
}) {
    function handleKeyDown(e) {
        // Shift + Enter は改行
        if (e.key === "Enter" && e.shiftKey) {
            return;
        }

        // Enter送信
        if (e.key === "Enter") {
            e.preventDefault();

            // 空文字送信防止
            if (!question.trim()) {
                return;
            }

            handleAsk();
        }
    }

    return (
        <div className="flex gap-3 items-end">
            <textarea
                className="
                    flex-1
                    border
                    rounded-2xl
                    px-4
                    py-3
                    resize-none
                    focus:outline-none
                    focus:ring-2
                    focus:ring-blue-400
                "
                rows={2}
                placeholder="質問してください..."
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={handleKeyDown}
            />

            <button
                className="
                    bg-blue-500
                    text-white
                    px-6
                    py-3
                    rounded-2xl
                    hover:bg-blue-600
                    disabled:bg-gray-400
                "
                onClick={handleAsk}
                disabled={loading || !question.trim()}
            >
                {loading ? "送信中..." : "送信"}
            </button>
        </div>
    );
}
