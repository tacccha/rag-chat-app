import { useState, useEffect, useRef } from "react";

import QuestionInput from "../components/QuestionInput";

import UploadSection from "../components/UploadSection";

import ChatHistory from "../components/ChatHistory";

import DocumentsList from "../components/DocumentsList";

export default function Home() {
    // API URL
    const API_URL = import.meta.env.VITE_API_URL;

    // =========================
    // state
    // =========================

    // 質問入力値
    const [question, setQuestion] = useState("");

    // upload対象file
    const [file, setFile] = useState(null);

    // 登録済みdocument一覧
    const [documents, setDocuments] = useState([]);

    // ローディング表示
    const [loading, setLoading] = useState(false);

    // エラー
    const [error, setError] = useState("");

    // 会話履歴
    const [histories, setHistories] = useState([]);

    // Sidebar開閉
    const [sidebarOpen, setSidebarOpen] = useState(true);

    // アップロード中
    const [uploading, setUploading] = useState(false);

    // chat最下部ref
    const bottomRef = useRef(null);

    // file input制御用
    const fileInputRef = useRef(null);

    // =========================
    // 質問送信
    // =========================

    async function handleAsk() {
        // 空送信防止
        if (!question.trim()) {
            return;
        }

        try {
            // loading開始
            setLoading(true);

            // エラー初期化
            setError("");

            // FastAPIへHTTP通信
            const response = await fetch(
                `${API_URL}/ask`,

                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json",
                    },

                    body: JSON.stringify({
                        question: question,
                    }),
                },
            );

            // FastAPI返却JSON取得
            const data = await response.json();

            // 会話履歴追加
            setHistories((prev) => [
                ...prev,

                {
                    question: question,

                    answer: data.answer.answer,

                    sources: data.answer.sources,
                },
            ]);

            // 入力欄クリア
            setQuestion("");
        } catch (err) {
            console.error(err);

            setError("エラーが発生しました");
        } finally {
            // loading終了
            setLoading(false);
        }
    }

    // =========================
    // PDF upload
    // =========================

    async function handleUpload() {
        if (!file) {
            return;
        }

        // FormData生成
        const formData = new FormData();

        // file追加
        formData.append("file", file);

        try {
            // アップロード開始
            setUploading(true);

            const response = await fetch(
                `${API_URL}/upload`,

                {
                    method: "POST",
                    body: formData,
                },
            );

            const data = await response.json();

            alert(data.message);

            // 一覧再取得
            await loadDocuments();

            // file初期化
            setFile(null);

            if (fileInputRef.current) {
                fileInputRef.current.value = "";
            }
        } catch (err) {
            console.error(err);

            alert("アップロードに失敗しました");
        } finally {
            // アップロード終了
            setUploading(false);
        }
    }

    // =========================
    // document一覧取得
    // =========================

    async function loadDocuments() {
        try {
            const response = await fetch(`${API_URL}/documents/raw`);

            const data = await response.json();

            setDocuments(data.documents);
        } catch (err) {
            console.error(err);

            setError("Document取得に失敗しました");
        }
    }

    // =========================
    // document削除
    // =========================

    async function handleDelete(filename) {
        const confirmDelete = window.confirm(`${filename} を削除しますか？`);

        if (!confirmDelete) {
            return;
        }

        try {
            const response = await fetch(
                `${API_URL}/delete`,

                {
                    method: "DELETE",

                    headers: {
                        "Content-Type": "application/json",
                    },

                    body: JSON.stringify({
                        filename: filename,
                    }),
                },
            );

            const data = await response.json();

            alert(data.message);

            // document一覧再取得
            loadDocuments();
        } catch (err) {
            console.error(err);

            alert("削除に失敗しました");
        }
    }

    // =========================
    // 初回表示時処理
    // =========================

    useEffect(() => {
        loadDocuments();
    }, []);

    // =========================
    // localStorageから履歴復元
    // =========================

    useEffect(() => {
        const savedHistories = localStorage.getItem("rag_histories");

        if (savedHistories) {
            setHistories(JSON.parse(savedHistories));
        }
    }, []);

    // =========================
    // histories更新時
    // =========================

    useEffect(() => {
        // localStorage保存

        localStorage.setItem("rag_histories", JSON.stringify(histories));

        // 最下部scroll

        bottomRef.current?.scrollIntoView({
            behavior: "smooth",
        });
    }, [histories]);

    return (
        <div
            className="
                h-screen
                bg-gray-100
                flex
            "
        >
            {/* Sidebar */}

            <div
                className={`
                    bg-white
                    border-r
                    transition-all
                    duration-300
                    overflow-hidden
                    ${sidebarOpen ? "w-[320px]" : "w-[70px]"}
                `}
            >
                <div
                    className="
                        p-6
                        flex
                        justify-between
                        items-center
                    "
                >
                    {sidebarOpen && (
                        <h1
                            className="
                                    text-4xl
                                    font-bold
                                "
                        >
                            RAG Chat
                        </h1>
                    )}

                    <button
                        className="
                            border
                            rounded-lg
                            px-3
                            py-2
                            hover:bg-gray-100
                            cursor-pointer
                        "
                        onClick={() => setSidebarOpen(!sidebarOpen)}
                    >
                        {sidebarOpen ? "←" : "→"}
                    </button>
                </div>

                {sidebarOpen && (
                    <div className="px-6 pb-6">
                        <UploadSection
                            file={file}
                            setFile={setFile}
                            handleUpload={handleUpload}
                            uploading={uploading}
                            fileInputRef={fileInputRef}
                        />

                        <DocumentsList
                            documents={documents}
                            handleDelete={handleDelete}
                        />
                    </div>
                )}
            </div>

            {/* Main */}

            <div
                className="
                    flex
                    flex-col
                    flex-1
                    bg-white
                "
            >
                {/* Header */}

                <div
                    className="
                        border-b
                        px-6
                        py-5
                        flex
                        justify-between
                        items-center
                    "
                >
                    <div>
                        <h2
                            className="
                                text-3xl
                                font-bold
                            "
                        >
                            AI Assistant
                        </h2>

                        <p
                            className="
                                text-sm
                                text-gray-500
                                mt-1
                            "
                        >
                            PDFベース社内文書検索 RAGシステム
                        </p>
                    </div>

                    <div
                        className="
                            text-green-500
                            border
                            border-green-300
                            rounded-full
                            px-4
                            py-1
                            text-sm
                        "
                    >
                        ● Online
                    </div>
                </div>

                {/* Error */}

                {error && (
                    <div
                        className="
                                px-6
                                py-3
                                text-red-500
                                border-b
                                bg-red-50
                            "
                    >
                        {error}
                    </div>
                )}

                {/* Chat History */}

                <ChatHistory
                    histories={histories}
                    bottomRef={bottomRef}
                    loading={loading}
                />

                {/* Input Area */}

                <div
                    className="
                        border-t
                        bg-white
                        p-4
                    "
                >
                    <QuestionInput
                        question={question}
                        setQuestion={setQuestion}
                        handleAsk={handleAsk}
                        loading={loading}
                    />
                </div>
            </div>
            {uploading && (
                <div
                    className="
                        fixed
                        inset-0
                        bg-black/40
                        flex
                        items-center
                        justify-center
                        z-50
                    "
                >
                    <div
                        className="
                            bg-white
                            px-10
                            py-8
                            rounded-2xl
                            shadow-xl
                            text-center
                        "
                    >
                        <div
                            className="
                                animate-spin
                                rounded-full
                                h-16
                                w-16
                                border-[6px]
                                border-gray-200
                                border-t-blue-500
                                mx-auto
                            "
                        />
                        <p className="mt-6 font-semibold">
                            PDFを解析しています...
                        </p>
                        <p className="text-sm text-gray-500 mt-2">
                            ファイル保存 → Chunk作成 → Embedding生成 →
                            ChromaDB登録
                        </p>
                    </div>
                </div>
            )}
        </div>
    );
}
