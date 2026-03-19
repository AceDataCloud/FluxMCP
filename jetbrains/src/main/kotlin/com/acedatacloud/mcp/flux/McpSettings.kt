package com.acedatacloud.mcp.flux

import com.intellij.openapi.application.ApplicationManager
import com.intellij.openapi.components.PersistentStateComponent
import com.intellij.openapi.components.Service
import com.intellij.openapi.components.State
import com.intellij.openapi.components.Storage

@Service(Service.Level.APP)
@State(name = "McpSettings_flux", storages = [Storage("McpFluxSettings.xml")])
class McpSettings : PersistentStateComponent<McpSettings.State> {

    data class State(
        var apiToken: String = "",
        var hasShownSetupNotification: Boolean = false
    )

    private var myState = State()

    override fun getState(): State = myState

    override fun loadState(state: State) {
        myState = state
    }

    companion object {
        fun getInstance(): McpSettings =
            ApplicationManager.getApplication().getService(McpSettings::class.java)
    }

    fun getStdioConfig(): String {
        val token = myState.apiToken.ifEmpty { "YOUR_API_TOKEN" }
        return """{"mcpServers": {"flux": {"command": "uvx", "args": ["mcp-flux-pro"], "env": {"ACEDATACLOUD_API_TOKEN": "$$token"}}}}"""
    }

    fun getHttpConfig(): String {
        val token = myState.apiToken.ifEmpty { "YOUR_API_TOKEN" }
        return """{"mcpServers": {"flux": {"url": "https://flux.mcp.acedata.cloud/mcp", "headers": {"Authorization": "Bearer $$token"}}}}"""
    }
}
