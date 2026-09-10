<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Logo Landscape - Visual Identity Research</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 font-sans antialiased">

  <div class="flex h-screen overflow-hidden">
    
    <!-- Sidebar / Filters -->
    <aside class="w-72 bg-white border-r border-slate-200 flex flex-col justify-between hidden lg:flex">
      <div>
        <!-- Logo Area -->
        <div class="p-6 border-b border-slate-100 flex items-center justify-between">
          <h1 class="text-lg font-bold tracking-tight text-slate-900">Logo Landscape</h1>
        </div>

        <!-- Navigation Tabs -->
        <div class="px-6 py-4 flex gap-2">
          <button class="flex-1 bg-slate-900 text-white text-sm font-medium py-2 px-4 rounded-full shadow-sm">Gallery</button>
          <button class="flex-1 bg-slate-100 text-slate-600 hover:bg-slate-200 text-sm font-medium py-2 px-4 rounded-full transition">Analytics</button>
        </div>

        <!-- Filter Accordions -->
        <div class="px-6 py-2 space-y-4">
          <div class="flex items-center justify-between text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
            <span>Filters</span>
            <button class="hover:text-slate-600 transition">Reset</button>
          </div>

          <div class="relative">
            <input type="text" placeholder="Search organisation..." class="w-full bg-slate-50 border border-slate-200 rounded-lg text-sm px-3 py-2 focus:outline-none focus:ring-2 focus:ring-slate-900/10">
          </div>

          <div class="space-y-2 pt-2">
            <button class="w-full flex items-center justify-between p-2.5 rounded-lg border border-slate-200 text-sm font-medium text-slate-700 hover:bg-slate-50 transition">
              <span class="flex items-center gap-2">🏛️ Organization & Location</span>
              <span class="text-slate-400">›</span>
            </button>
            <button class="w-full flex items-center justify-between p-2.5 rounded-lg border border-slate-200 text-sm font-medium text-slate-700 hover:bg-slate-50 transition">
              <span class="flex items-center gap-2">📐 Logo Details & Design</span>
              <span class="text-slate-400">›</span>
            </button>
            <button class="w-full flex items-center justify-between p-2.5 rounded-lg border border-slate-200 text-sm font-medium text-slate-700 hover:bg-slate-50 transition">
              <span class="flex items-center gap-2">🎨 Colors</span>
              <span class="text-slate-400">›</span>
            </button>
            <button class="w-full flex items-center justify-between p-2.5 rounded-lg border border-slate-200 text-sm font-medium text-slate-700 hover:bg-slate-50 transition">
              <span class="flex items-center gap-2">✍️ Type Style</span>
              <span class="text-slate-400">›</span>
            </button>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main Content Area -->
    <main class="flex-1 flex flex-col overflow-y-auto">
      
      <!-- Top Bar -->
      <header class="bg-white border-b border-slate-200 px-8 py-4 flex items-center justify-between sticky top-0 z-10">
        <span class="text-sm font-medium text-slate-500">Visual Identity Research</span>
        <span class="text-sm font-semibold text-slate-900">123 Identities</span>
      </header>

      <div class="p-8 max-w-7xl mx-auto w-full space-y-6">
        
        <!-- Editorial Summary Banner -->
        <div class="bg-slate-100 border border-slate-200/80 rounded-xl p-4 flex items-center justify-between text-slate-600 font-medium text-sm">
          <span>Editorial Summary</span>
          <span class="text-slate-400 text-lg">⌄</span>
        </div>

        <!-- Active Filter Pills & Sorting -->
        <div class="flex flex-wrap items-center justify-between gap-4 bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <div class="flex flex-wrap items-center gap-2">
            <span class="inline-flex items-center gap-1.5 bg-slate-900 text-white text-xs font-medium px-3 py-1.5 rounded-full">
              Govt. <button class="hover:text-slate-300">×</button>
            </span>
            <span class="inline-flex items-center gap-1.5 bg-slate-900 text-white text-xs font-medium px-3 py-1.5 rounded-full">
              Blue <button class="hover:text-slate-300">×</button>
            </span>
            <span class="inline-flex items-center gap-1.5 bg-slate-900 text-white text-xs font-medium px-3 py-1.5 rounded-full">
              Abstract <button class="hover:text-slate-300">×</button>
            </span>
            <button class="text-xs font-semibold text-slate-500 hover:text-slate-800 ml-2">Clear All</button>
          </div>
          <div class="flex items-center gap-2 text-sm text-slate-500">
            <span>Sort</span>
            <select class="bg-slate-50 border border-slate-200 rounded-lg px-3 py-1.5 text-sm font-medium text-slate-700 focus:outline-none">
              <option>Name A–Z</option>
              <option>Name Z–A</option>
            </select>
          </div>
        </div>

        <!-- Results Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          
          <!-- Card 1 -->
          <div class="bg-white rounded-2xl border border-slate-200 shadow-xs hover:shadow-md transition flex flex-col overflow-hidden">
            <div class="h-48 bg-slate-50 flex items-center justify-center p-6 border-b border-slate-100">
              <!-- Placeholder for logo asset -->
              <div class="w-28 h-28 rounded-full bg-white border border-slate-200 shadow-xs flex items-center justify-center text-xs font-bold text-slate-400">LOGO</div>
            </div>
            <div class="p-5 flex-1 flex flex-col justify-between space-y-4">
              <h3 class="font-semibold text-slate-900 text-base leading-snug">Sathyabama Institute of Science and Technology Deemed University, Chennai</h3>
              <div class="grid grid-cols-2 gap-2 pt-2 border-t border-slate-100 text-xs">
                <div><span class="text-slate-400 block">Shape</span><span class="font-medium text-slate-700">Circle</span></div>
                <div><span class="text-slate-400 block">Sector</span><span class="font-medium text-slate-700">Private - For - Profit</span></div>
                <div><span class="text-slate-400 block">Color</span><span class="font-medium text-slate-700">Tetradic</span></div>
                <div><span class="text-slate-400 block">Country</span><span class="font-medium text-slate-700">India</span></div>
              </div>
              <div class="pt-2">
                <span class="text-[11px] font-semibold text-indigo-600 hover:text-indigo-700 cursor-pointer tracking-wide">TAP CARD TO FLIP DETAILS ↻</span>
              </div>
            </div>
          </div>

          <!-- Card 2 -->
          <div class="bg-white rounded-2xl border border-slate-200 shadow-xs hover:shadow-md transition flex flex-col overflow-hidden">
            <div class="h-48 bg-slate-50 flex items-center justify-center p-6 border-b border-slate-100">
              <div class="w-28 h-28 rounded-full bg-white border border-slate-200 shadow-xs flex items-center justify-center text-xs font-bold text-slate-400">LOGO</div>
            </div>
            <div class="p-5 flex-1 flex flex-col justify-between space-y-4">
              <h3 class="font-semibold text-slate-900 text-base leading-snug">Tata Memorial Centre</h3>
              <div class="grid grid-cols-2 gap-2 pt-2 border-t border-slate-100 text-xs">
                <div><span class="text-slate-400 block">Shape</span><span class="font-medium text-slate-700">Circle</span></div>
                <div><span class="text-slate-400 block">Sector</span><span class="font-medium text-slate-700">Govt.</span></div>
                <div><span class="text-slate-400 block">Color</span><span class="font-medium text-slate-700">Tetradic</span></div>
                <div><span class="text-slate-400 block">Country</span><span class="font-medium text-slate-700">India</span></div>
              </div>
              <div class="pt-2">
                <span class="text-[11px] font-semibold text-indigo-600 hover:text-indigo-700 cursor-pointer tracking-wide">TAP CARD TO FLIP DETAILS ↻</span>
              </div>
            </div>
          </div>

          <!-- Card 3 -->
          <div class="bg-white rounded-2xl border border-slate-200 shadow-xs hover:shadow-md transition flex flex-col overflow-hidden">
            <div class="h-48 bg-slate-50 flex items-center justify-center p-6 border-b border-slate-100">
              <div class="w-28 h-28 rounded-full bg-white border border-slate-200 shadow-xs flex items-center justify-center text-xs font-bold text-slate-400">LOGO</div>
            </div>
            <div class="p-5 flex-1 flex flex-col justify-between space-y-4">
              <h3 class="font-semibold text-slate-900 text-base leading-snug">Tata Memorial Hospital</h3>
              <div class="grid grid-cols-2 gap-2 pt-2 border-t border-slate-100 text-xs">
                <div><span class="text-slate-400 block">Shape</span><span class="font-medium text-slate-700">Circle</span></div>
                <div><span class="text-slate-400 block">Sector</span><span class="font-medium text-slate-700">Govt.</span></div>
                <div><span class="text-slate-400 block">Color</span><span class="font-medium text-slate-700">Complimentary</span></div>
                <div><span class="text-slate-400 block">Country</span><span class="font-medium text-slate-700">India</span></div>
              </div>
              <div class="pt-2">
                <span class="text-[11px] font-semibold text-indigo-600 hover:text-indigo-700 cursor-pointer tracking-wide">TAP CARD TO FLIP DETAILS ↻</span>
              </div>
            </div>
          </div>

        </div>

      </div>
    </main>

  </div>

</body>
</html>
