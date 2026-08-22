import React, { useState, useEffect, useRef } from 'react';
import { chatApi, driveApi } from '../../api/services';
import { useAuth } from '../../context/AuthContext';
import {
  Bot,
  User,
  Sparkles,
  Send,
  HelpCircle,
  Briefcase,
  GitFork,
  ArrowRight,
  Lightbulb,
  CheckCircle2,
  AlertCircle,
  Layers,
} from 'lucide-react';

const AIChatAssistant = () => {
  const { user } = useAuth();
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      sender: 'ai',
      text: `Hello ${user?.full_name || 'there'}! I am your AI Placement & Career Assistant powered by Neo4j GraphRAG. I can explain your eligibility for placement drives, analyze skill gaps, and recommend career growth paths based on live database graphs. How can I help you today?`,
      timestamp: new Date(),
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [selectedDriveId, setSelectedDriveId] = useState('');
  const [drives, setDrives] = useState([]);
  const [faqs, setFaqs] = useState([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const initData = async () => {
      try {
        const [driveList, faqList] = await Promise.all([
          driveApi.listDrives('PUBLISHED', 0, 50).catch(() => []),
          chatApi.getFAQs().catch(() => []),
        ]);
        setDrives(driveList || []);
        setFaqs(faqList || []);
      } catch (err) {
        console.error('Failed to load chat metadata:', err);
      }
    };
    initData();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSendMessage = async (customQuery = null) => {
    const query = (customQuery || inputText).trim();
    if (!query || loading) return;

    const userMessageId = Date.now().toString();
    const newMsg = {
      id: userMessageId,
      sender: 'user',
      text: query,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, newMsg]);
    if (!customQuery) setInputText('');
    setLoading(true);

    try {
      const response = await chatApi.askAssistant(query, selectedDriveId || null);

      const aiMsg = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text: response.answer,
        graphContext: response.retrieved_graph_context,
        suggestedSkills: response.suggested_skills_to_learn || [],
        recommendedDrives: response.recommended_drives || [],
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      console.error('Chat error:', err);
      const errorMsg = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text:
          err.response?.data?.detail ||
          'I encountered an issue querying the placement knowledge graph or LLM engine. Please ensure your Ollama service is reachable.',
        isError: true,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden">
      {/* Chat Top Header */}
      <div className="p-4 bg-slate-50 border-b border-slate-200 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-purple-500/20">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
              GraphRAG Career Assistant
              <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-purple-100 text-purple-700">
                Neo4j + LLM
              </span>
            </h2>
            <p className="text-xs text-slate-500">
              Grounded multi-hop reasoning over student skills and drive criteria
            </p>
          </div>
        </div>

        {/* Drive Context Selector */}
        <div className="flex items-center gap-2 w-full sm:w-auto">
          <span className="text-xs font-bold text-slate-400 shrink-0">Drive Context:</span>
          <select
            value={selectedDriveId}
            onChange={(e) => setSelectedDriveId(e.target.value)}
            className="w-full sm:w-56 px-3 py-1.5 bg-white border border-slate-200 rounded-xl text-xs font-medium focus:ring-2 focus:ring-purple-500"
          >
            <option value="">General Inquiries (No Drive)</option>
            {drives.map((d) => (
              <option key={d.id} value={d.id}>
                {d.company_name} — {d.title}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Messages Thread */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex gap-3 max-w-3xl ${
              msg.sender === 'user' ? 'ml-auto flex-row-reverse' : 'mr-auto'
            }`}
          >
            {/* Avatar */}
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center text-white shrink-0 text-xs font-bold ${
                msg.sender === 'user' ? 'bg-brand-600' : 'bg-purple-600'
              }`}
            >
              {msg.sender === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
            </div>

            {/* Message Bubble */}
            <div
              className={`rounded-2xl p-4 text-sm leading-relaxed ${
                msg.sender === 'user'
                  ? 'bg-brand-600 text-white rounded-tr-none shadow-md shadow-brand-500/10'
                  : msg.isError
                  ? 'bg-rose-50 border border-rose-200 text-rose-800 rounded-tl-none'
                  : 'bg-slate-50 border border-slate-200 text-slate-800 rounded-tl-none'
              }`}
            >
              <p className="whitespace-pre-wrap">{msg.text}</p>

              {/* Suggested Skills to Learn */}
              {msg.suggestedSkills?.length > 0 && (
                <div className="mt-3 pt-3 border-t border-slate-200/60">
                  <span className="text-xs font-bold text-purple-700 flex items-center gap-1 mb-1.5">
                    <Lightbulb className="w-3.5 h-3.5" /> High-Impact Skills to Acquire:
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {msg.suggestedSkills.map((s, idx) => (
                      <span
                        key={idx}
                        className="px-2.5 py-0.5 bg-purple-100 text-purple-800 rounded-lg text-xs font-semibold"
                      >
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Recommended Drives */}
              {msg.recommendedDrives?.length > 0 && (
                <div className="mt-3 pt-3 border-t border-slate-200/60">
                  <span className="text-xs font-bold text-slate-700 flex items-center gap-1 mb-1.5">
                    <Briefcase className="w-3.5 h-3.5 text-brand-600" /> Recommended Drives:
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {msg.recommendedDrives.map((d, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-0.5 bg-brand-50 text-brand-700 rounded-md text-xs font-medium"
                      >
                        {d}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Retrieved Graph Context Inspector */}
              {msg.graphContext && Object.keys(msg.graphContext).length > 0 && (
                <details className="mt-3 pt-2 border-t border-slate-200/60 text-xs cursor-pointer group">
                  <summary className="font-semibold text-slate-500 group-hover:text-slate-800 flex items-center gap-1 select-none">
                    <GitFork className="w-3.5 h-3.5 text-indigo-500" />
                    Inspect Graph Traversal & Policy Facts
                  </summary>
                  <div className="mt-2 p-3 bg-white border border-slate-200 rounded-xl text-[11px] font-mono text-slate-700 overflow-x-auto max-h-40">
                    <pre>{JSON.stringify(msg.graphContext, null, 2)}</pre>
                  </div>
                </details>
              )}

              <span className="text-[10px] opacity-60 block mt-2 text-right">
                {new Date(msg.timestamp).toLocaleTimeString([], {
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </span>
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex gap-3 max-w-3xl mr-auto">
            <div className="w-8 h-8 rounded-full bg-purple-600 flex items-center justify-center text-white shrink-0">
              <Bot className="w-4 h-4" />
            </div>
            <div className="p-4 bg-slate-50 border border-slate-200 rounded-2xl rounded-tl-none flex items-center gap-2 text-xs font-semibold text-slate-500">
              <div className="w-3 h-3 border-2 border-purple-500 border-t-transparent rounded-full animate-spin" />
              <span>Traversing Neo4j Placement Graph & Generating Grounded Answer...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Quick FAQs Chips */}
      {faqs.length > 0 && (
        <div className="px-4 py-2 bg-slate-50 border-t border-slate-100 flex items-center gap-2 overflow-x-auto">
          <span className="text-[11px] font-bold text-slate-400 shrink-0 flex items-center gap-1">
            <HelpCircle className="w-3.5 h-3.5" /> FAQs:
          </span>
          {faqs.slice(0, 4).map((faq, idx) => (
            <button
              key={idx}
              onClick={() => handleSendMessage(faq.question || faq.q)}
              className="px-3 py-1 bg-white hover:bg-purple-50 hover:text-purple-700 hover:border-purple-200 border border-slate-200 rounded-full text-xs font-medium text-slate-600 whitespace-nowrap transition-all shadow-2xs"
            >
              {faq.question || faq.q}
            </button>
          ))}
        </div>
      )}

      {/* Input Form */}
      <div className="p-4 bg-white border-t border-slate-200">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSendMessage();
          }}
          className="flex gap-2"
        >
          <input
            type="text"
            placeholder={
              selectedDriveId
                ? 'Ask about your eligibility or skill match for this drive...'
                : 'Ask anything about placements, your skills, or preparation...'
            }
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            disabled={loading}
            className="flex-1 px-4 py-3 bg-slate-50 border border-slate-200 rounded-2xl text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:bg-white transition-all disabled:opacity-60"
          />
          <button
            type="submit"
            disabled={loading || !inputText.trim()}
            className="px-5 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold text-sm rounded-2xl shadow-md shadow-purple-500/20 transition-all disabled:opacity-50 flex items-center gap-2"
          >
            <Send className="w-4 h-4" />
            <span className="hidden sm:inline">Ask AI</span>
          </button>
        </form>
      </div>
    </div>
  );
};

export default AIChatAssistant;
