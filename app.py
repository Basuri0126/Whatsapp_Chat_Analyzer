import streamlit as st
import preprocessor
import needed_function
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
import plotly.express as px



def initialize_session():
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.data_loaded = False


def main():
    st.set_page_config(layout='wide', page_title='Chat', page_icon='img/students.png')
    custom_css = """
    <style>
    /* Contents of hide_git_icon.css */
    </style>
    """

    st.markdown(custom_css, unsafe_allow_html=True)

    initialize_session()
    st.title('Whatsapp Chat Analysis')
    st.markdown("#### Please wait after selecting any Option Because it takes time to Analyze `\U0001F64F`")
    st.markdown('<p style="font-size: 24px; color: blue;">Thank You 😃 😍</p>', unsafe_allow_html=True)
    st.sidebar.markdown("""
        <h2 style="text-align:center; color: #0056b3; font-size: 20px">Upload Your whatsapp Chat</h2>
        <hr style="border:1px solid #0056b3;">
    """, unsafe_allow_html=True)


    # --------file handling-------
    upload_file = st.sidebar.file_uploader('Choose a file')
    if upload_file is not None:
        bytes_data = upload_file.getvalue()
        data = bytes_data.decode('utf-8')
        df = preprocessor.preprocessor(data)

        st.divider()
        # fetch unique users
        users_list = df['users'].unique().tolist()
        users_list.sort()
        users_list.insert(0, 'Overall Group')
        selected_user = st.sidebar.selectbox('Select a Course Mate', users_list)


        if st.sidebar.button('Show Details'):

            total_message, word, num_media_share, links = needed_function.fetch_data(selected_user, df)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown('### Total Message in Group')
                st.subheader(total_message)

            with col2:
                st.markdown('### Total Words Type')
                st.subheader(word)

            with col3:
                st.markdown('### Total Media Share')
                st.subheader(num_media_share)

            with col4:
                st.markdown('### Total Links Share')
                st.subheader(links)

            st.divider()
            if selected_user == 'Overall Group':
                st.title('Top Chatter in group')
                top_chatter, top_user_pct = needed_function.fetch_top_chatter(df)

                x = top_chatter.index
                y = top_chatter.values

                # fig, ax = plt.subplots(figsize=(11, 7.5))

                col1, col2 = st.columns(2)

                with col1:
                    # ax.bar(x, y,  color="slateblue")
                    # plt.ylabel('Users', fontsize=18)
                    # plt.xlabel('Number Of Chat', fontsize=18)
                    # plt.xticks(rotation='vertical')
                    # plt.tick_params(axis='x', labelsize=18)
                    # plt.tick_params(axis='y', labelsize=18)

                    # for i in range(len(x)):
                    #     plt.text(x[i], y[i], str(y[i]), ha='center', va='bottom')
                    # st.pyplot(fig)

                    fig = go.Figure(data=[go.Bar(x=x, y=y, marker=dict(color="slateblue"))])
                    fig.update_layout(
                        title='Number of Chats per User (3D)',
                        scene=dict(
                            xaxis=dict(title='Users'),
                            yaxis=dict(title='Number Of Chat'),
                            zaxis=dict(title='Count'),
                        )
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    st.dataframe(top_user_pct, use_container_width=True)

            st.divider()
            # -----------------------world cloud for most common words-----------------
            st.title('Most use words show Bigger in Size')
            df_wc = needed_function.create_wordcloud(selected_user, df)

            if df_wc is None:
                st.title(f'Not any word found OR write by {selected_user}')
            else:
                fig, ax = plt.subplots()
                ax.imshow(df_wc, interpolation='bilinear')
                plt.axis('off')
                plt.tight_layout(pad=0)
                st.pyplot(fig, use_container_width=True)

            st.divider()
            # ----------------bar plot for most common words--------------
            st.title('Most Common Words Uses by {}'.format(selected_user))
            most_common_word = needed_function.most_common_words(selected_user, df)

            fig = go.Figure(data=[go.Bar(x=most_common_word[0], y=most_common_word[1],
                                         marker=dict(color="Medium Aquamarine"))])
            fig.update_layout(
                yaxis=dict(title='Number of Count', title_font=dict(size=25), tickfont=dict(size=14)),
                xaxis=dict(title='Words', title_font=dict(size=25), tickfont=dict(size=14)),
            )
            st.plotly_chart(fig, use_container_width=True)

            # --------------emoji-----------------------
            em_df = needed_function.find_emoji(selected_user, df)
            if em_df.empty:
                st.title(f'NO Emoji Sent by the {selected_user}')
            else:
                st.title('Emoji Analysis')
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(em_df)
                with col2:
                    unique_emojis = list(em_df[0].head(20))
                    emoji_freq = list(em_df[1])

                    fig = go.Figure(
                        data=[go.Pie(
                            labels=unique_emojis, values=emoji_freq, hole=0.4
                        )])

                    colors = ['rgb(63, 112, 225)', 'rgb(46, 204, 113)', 'rgb(52, 152, 219)',
                              'rgb(241, 196, 15)', 'rgb(230, 126, 34)', 'rgb(155, 89, 182)']
                    fig.update_traces(hoverinfo='label+percent',
                                      textinfo='value', textfont_size=20,
                                      marker=dict(colors=colors,
                                      line=dict(color='#000000', width=2))
                                      )

                    fig.update_layout(title='Emoji Distribution', autosize=True)

                    emoji_labels = [emoji.encode('utf-8').decode('utf-8') for emoji in unique_emojis]
                    fig.update_traces(text=emoji_labels)
                    st.plotly_chart(fig, use_container_width=True)

            # line chart month
            st.divider()
            st.title('Monthly Message Count')
            time_df = needed_function.daily_month(selected_user, df)
            fig = go.Figure()

            fig.add_trace(go.Scatter(x=time_df['time'], y=time_df['message'], mode='lines+markers',
                                     text=time_df['month_num'], textposition='top center',
                                     line=dict(color='rgb(46, 204, 113)'), marker=dict(size=8),
                                     hovertemplate='%{x|%b-%Y}: %{y} messages'))

            fig.update_layout(
                              xaxis_title='Month-Year',
                              yaxis_title='Number of Messages')
            st.plotly_chart(fig, use_container_width=True)

            # day month plot
            st.divider()
            col1, col2 = st.columns(2)

            with col1:
                st.header('Busy Days')
                day_df = needed_function.daily_day(selected_user, df)
                fig = go.Figure()

                fig.add_trace(go.Bar(x=day_df['day_name'], y=day_df['messageCount'], marker={'color': 'rgb(191, 46, 179)'}))

                fig.update_layout(
                    xaxis_title='day',
                    yaxis_title='Number of Messages')
                st.plotly_chart(fig)

            with col2:
                st.header('Busy Months')
                month_df = needed_function.daily_month_bar(selected_user, df)
                fig = go.Figure()
                fig.add_trace(go.Bar(x=month_df['month'], y=month_df['messageCount'], marker={'color': 'rgb(57, 22, 161)'}))

                fig.update_layout(
                    xaxis_title='Month',
                    yaxis_title='Number of Messages')
                st.plotly_chart(fig)

            # heatmap
            st.divider()
            st.title('Heatmap of Messages by Day and Period')
            heat_df = needed_function.heatmap_hour(selected_user, df)
            fig, ax = plt.subplots(figsize=(10, 5), facecolor='#2B2B2B')
            sns.heatmap(heat_df, ax=ax, vmax=heat_df.values.max())
            ax.set_xlabel('Period', color='white')
            ax.set_ylabel('Day', color='white')

            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            st.pyplot(fig)

            # animated graph
            st.divider()
            st.markdown("### Let's see how the chatter patterns change over time!")
            animated_df = needed_function.top_10(selected_user, df)
            fig = px.scatter(animated_df, x='day_name', y='month', size='message_count', color='users', size_max=100,
                             hover_name='users', animation_frame='month', text='data_info', range_color=[1, len(df['users'].unique())],
                             range_y=[1, 12])

            fig.update_layout(title=f'Group Chat Activity for {selected_user}',
                              xaxis_title='Day of the Week',
                              yaxis_title='Month',
                              showlegend=True,
                              legend=dict(font=dict(color='brown')),
                              sliders=dict(font=dict(color='black')), height=600)
            fig.update_traces(textfont=dict(color='black'))

            st.plotly_chart(fig, use_container_width=True)

            # top chatter per month bar graph animated
            st.divider()

            if selected_user == 'Overall Group':
                st.title('Top Chatters by Message Count for Each Month')
                monthly_message_count = df.groupby(['month', 'users'])['message'].count().reset_index()
                monthly_message_count.rename(columns={'message': 'message_count'}, inplace=True)

                top_chatters = (
                    monthly_message_count.groupby('month')
                    .apply(lambda x: x.nlargest(20, 'message_count'))
                    .reset_index(drop=True)
                )

                fig = px.bar(top_chatters, x='users', y='message_count', animation_frame='month',
                             category_orders={'users': top_chatters['users'].tolist()},
                             labels={'message_count': 'Message Count'},
                             range_y=[0, top_chatters['message_count'].max() + 50],
                             color_discrete_sequence=px.colors.qualitative.Set3)

                fig.update_layout(yaxis_title='Message Count', showlegend=False, margin=dict(t=50), height=600,
                                  updatemenus=[dict(
                                      type="buttons",
                                      buttons=[dict(
                                                    method="animate",
                                                    args=[None, {"frame": {"duration": 2000, "redraw": False}, }])])]
                                  )
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.title(f'Message Count for {selected_user} Over the Months')
                user_data = df[df['users'] == selected_user]
                fig.update_traces(marker_color='green')
                fig = px.bar(user_data, x='day_name', y='message_count', animation_frame='month',
                             labels={'week': 'Week', 'message_count': 'Message Count'},
                             range_y=[0, user_data['message_count'].max() + 10])

                fig.update_layout(showlegend=True, margin=dict(t=50))
                fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500
                st.plotly_chart(fig, use_container_width=True)

        st.sidebar.subheader("If You Don't know how to get Whatsapp Chat, Refer to Google")

if __name__ == "__main__":
    main()
