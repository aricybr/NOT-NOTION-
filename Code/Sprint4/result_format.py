 def show_all_tasks():
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
        tasks.sort(key=lambda t: (t['date'], priority_order.get(t['priority'],1)))

        for w in result_frame.winfo_children():
            w.destroy()

        # Header in display
        header = tk.Frame(result_frame, bg='#F7FAFC')
        header.pack(fill='x', pady=(0, 10), padx=5)
        tk.Label(header,
                 text="All Tasks",
                 font=('Segoe UI', 14, 'bold'),
                 bg='#F7FAFC').pack(side='left')
        tk.Button(header,
                  text="Add Task",
                  command=open_task_dialog,
                  bg='#3182CE', fg='white',
                  relief='flat',
                  padx=14, pady=5).pack(side='right')

        # Task list
        list_container = tk.Frame(result_frame, bg='#F7FAFC')
        list_container.pack(fill='both', expand=True)

        colors = {'High': '#FF0000', 'Medium': '#FFA500', 'Low': '#00BFFF'}

        for idx, task in enumerate(tasks):
            # Card frame
            card = tk.Frame(list_container,
                            bg='white',
                            bd=1, relief='solid',
                            padx=10, pady=8)
            card.pack(fill='x', pady=5, padx=5)

            # Checkbox
            completed_var = tk.BooleanVar(value=task.get('completed', False))
            chk = tk.Checkbutton(card,
                                 variable=completed_var,
                                 command=lambda i=idx, v=completed_var: toggle_complete(i, v),
                                 bg='white',
                                 activebackground='white',
                                 borderwidth=0)
            chk.pack(side='left')

            # Texts
            text_frame = tk.Frame(card, bg='white')
            text_frame.pack(side='left', fill='x', expand=True, padx=8)

            # Task name with optional overstrike
            name_font = tkFont.Font(family='Segoe UI',
                                    size=12,
                                    weight='bold',
                                    overstrike=task.get('completed', False))
            tk.Label(text_frame,
                     text=task['name'],
                     font=name_font,
                     bg='white').pack(anchor='w')

            # Date label
            tk.Label(text_frame,
                     text=task['date'],
                     font=('Segoe UI', 10),
                     bg='white').pack(anchor='w')

            # Details / subtitle
            tk.Label(text_frame,
                     text=task.get('details', ''),
                     font=('Segoe UI', 10),
                     fg='grey',
                     bg='white').pack(anchor='w')

            # Priority pill
            pill = tk.Label(card,
                            text=task['priority'],
                            bg=colors.get(task['priority'], 'grey'),
                            fg='white',
                            font=('Segoe UI', 9),
                            padx=6, pady=2)
            pill.pack(side='right')

            # Edit/Delete buttons container
            btn_frame = tk.Frame(card, bg='white')
            btn_frame.pack(side='right', padx=5)

            ttk.Button(btn_frame,
                       text="Edit",
                       command=lambda i=idx: open_task_dialog(i)).pack(side='left')

            ttk.Button(btn_frame,
                       text="Delete",
                       command=lambda i=idx: delete_task(i)).pack(side='left', padx=(5, 0))

        # Summary bar
        total = len(tasks)
        completed = sum(1 for t in tasks if t.get('completed'))
        high = sum(1 for t in tasks if t.get('priority') == 'High')
        summary = tk.Frame(result_frame, bg='#EDF2F7', padx=5, pady=5)
        summary.pack(fill='x', pady=(10, 5))
        tk.Label(summary,
                 text=f"{total} tasks total   •   {completed} completed   •   {high} high priority",
                 font=('Segoe UI', 10),
                 fg='grey',
                 bg='#EDF2F7').pack(side='left')
